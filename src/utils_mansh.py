import warnings
import os
warnings.filterwarnings("ignore", category=SyntaxWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import readchar
import pickle
import torch
import subprocess
import glob
from sentence_transformers import SentenceTransformer, util
from utils_generic import prntc, startdim_dim_flush, stopdim_dim_flush, cleanup_str, choose_param_value


def display_cached_models(models):
    startdim_dim_flush()
    prntc('Cached models : ')
    for modelID, (model_name, model_path) in enumerate(models):
        prntc(' ['+str(modelID)+'] : '+model_name)
    stopdim_dim_flush()
    return

def input_model_string():
    startdim_dim_flush()
    prntc('Check out available models at - https://www.sbert.net/docs/pretrained_models.html#sentence-embedding-models')
    model = input('Enter "Model Name" string (e.g. stsb-roberta-base-v2) : ').strip()
    stopdim_dim_flush()
    return model

def add_model(modelsdir, DEBUG=False):
    model = input_model_string()
    models = get_models(modelsdir)
    models_name = [m[0] for m in models]
    
    if model in models_name:
        prntc('Model already exists!', dim=True)
        return model

    data = setup_data_on_model(modelsdir, model, DEBUG=DEBUG)
    writeback(data, modelsdir, model)
    return model
    
def get_models(modelsdir):
    cached_filepaths = glob.glob(os.path.join(modelsdir,".cache_*.pickle"))
    models = [[os.path.basename(fp).replace('.cache_','').replace('.pickle',''),fp] for fp in cached_filepaths]
    return models

def writeback(data, modelsdir, model):
    cache_pkl_filepath = os.path.join(modelsdir, '.cache_' + model + '.pickle')
    with open(cache_pkl_filepath, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return

def query_on_corpus(data, cmd, query, max_n=None, delimiter='\n\n', REMOVE_STOPWORDS=False, DEBUG=False):
    update_status = update_data_on_command(data, cmd, delimiter=delimiter, DEBUG=DEBUG)  
    if update_status==-1:
        prntc('Error : No man page found for - '+cmd, dim=True)
        return None,None,-1
    model_data = data
    embedder = model_data['embedder']
    cmd_info = model_data['commands'][cmd]
    corpus = cmd_info['lines']
    corpus_embeddings = cmd_info['embeddings']    
    
    if REMOVE_STOPWORDS:
        corpus = [cleanup_str(c) for c in corpus]
        query = cleanup_str(query)

    bogus_idxs = [corpus_idx for corpus_idx,c in enumerate(corpus) if c.strip() == '']
    
    if max_n is None:
        top_k = len(corpus)
    else:
        top_k = min(max_n, len(corpus))
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]    
    cos_scores[bogus_idxs] = float(cos_scores.min()) # set bogus one to minimum priority    
    top_results = torch.topk(cos_scores, k=top_k)
    idxs = [idx for _, idx in zip(top_results[0], top_results[1])]
    return corpus, idxs, update_status

def setup_data_on_model(modelsdir, model, DEBUG=False):
    cache_pkl_filepath = os.path.join(modelsdir, '.cache_' + model + '.pickle')
    if os.path.exists(cache_pkl_filepath):        
        with open(cache_pkl_filepath, 'rb') as handle:
            data = pickle.load(handle)
        prntc('↦ Loaded existing pickle cache file.', dim=True, flag=DEBUG)
    else:
        data = {}
        embedder = SentenceTransformer(model)
        data = {'embedder':embedder, 'commands':{}}
        writeback(data, modelsdir, model)
        prntc('↦ No exising data found as the pickle cache file for model : ' + model + '. Set up a fresh one.', dim=True, flag=DEBUG)
    return data

def update_data_on_command(data, cmd, delimiter='\n\n', DEBUG=False):
    model_data = data
    
    cmd_data_found = True
    if cmd in model_data['commands']:
        cmd_data = data['commands'][cmd]
        if delimiter != cmd_data['delimiter']:
            cmd_data_found = False
    else:
        cmd_data_found = False
    
    if not cmd_data_found:
        result = subprocess.run(['man', cmd], stdout=subprocess.PIPE)
        if result.returncode != 0: # no man page found for this command        
            return -1
        
        corpus = result.stdout.decode('utf-8') .split(delimiter)
        prntc('Data not found for this command : ' + cmd + '. Setting it up. Creating embeddings ...', DEBUG, dim=True)
        prntc('Corpus length = '+str(len(corpus)), DEBUG, dim=True)
            
        embedder = data['embedder']
        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
        data['commands'][cmd] = {'delimiter':delimiter, 'lines':corpus, 'embeddings':corpus_embeddings}
        prntc('Saved new command embeddings into data variable!', DEBUG, dim=True)
        return 1
    else:
        return 0

def writeback_changes(data_updated, data, modelsdir, model):
    update_done = False
    if data_updated:
        prntc('\n↦ Data was updated. Cache it for future? (Yes[y]/No[any other key]) : ', end='', flush=True, dim=True)
        user_confirm_update_cache = readchar.readkey()
        if user_confirm_update_cache.lower() == 'y':
            writeback(data, modelsdir, model)
            update_done = True
            prntc('Saved!', dim=True)
        else:
            prntc('Not saved!', dim=True)
    return update_done

def change_model(modelsdir, models, model, data_updated, data, DEBUG_SETUP_DATA_ON_MODEL, DIMCOLOR=False, VANISH=False):
    models_name = [m[0] for m in models]
    model, param_changed = choose_param_value(list_of_options=models_name, currentval=model, DIMCOLOR=DIMCOLOR, VANISH=VANISH)        

    if param_changed:
        writeback_changes(data_updated, data, modelsdir, model)
        data_updated = False
        data = setup_data_on_model(modelsdir, model=model, DEBUG=DEBUG_SETUP_DATA_ON_MODEL)
    return model, data_updated, data

def get_available_commands_from_data(data, current_delimiter):
    available_cmds = []
    for k in data['commands'].keys():
        delim = data['commands'][k]['delimiter']
        if delim == current_delimiter:
            available_cmds.append(k)
    return available_cmds

def change_params(modelsdir, models, model, data_updated, data, delimiters, DELIMITER, VANISH=False, DEBUG_SHOW_LOADING=False, DIMCOLOR=False):
    prntc('\nChange model(m) or delimiter(d)? : ', dim=True, end='', flush=True)
    user_choice_model_delim = readchar.readkey().lower()
    if user_choice_model_delim == 'm':
        model, data_updated, data = change_model(modelsdir, models, model, data_updated, data, DEBUG_SETUP_DATA_ON_MODEL=DEBUG_SHOW_LOADING, DIMCOLOR=DIMCOLOR, VANISH=VANISH)
    elif user_choice_model_delim == 'd':
        DELIMITER, param_changed = choose_param_value(list_of_options=delimiters, currentval=DELIMITER, DIMCOLOR=DIMCOLOR, VANISH=VANISH)
    else:
        pass
    return model, data_updated, data, DELIMITER
