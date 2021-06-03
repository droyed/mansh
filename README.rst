mansh (man shell)
=================

|Py-Versions| |OS| |License|

**Why mansh?**

Going through Linux command man (manual) pages while trying to achieve a certain functionality isn't always a very comfortable experience, mostly because we might not be hitting the right keywords. For man pages that are short on words, this becomes a bigger issue. What if we could do a semantic search instead? Hence, ``mansh``!

**What is it?**

This repository provides a Python-based Linux shell, structured into two modes :

- **Manual semantic search mode** to hint and suggest the correct switch(es) for Linux commands given query strings for a natural language feel. Under the hoods this does a semantic similarity between blocks of Linux man pages against the given query and shows the most relevant switches for the task.
- Use those switches alongwith the command in a **normal console mode**.

Together these two modes try to get us closer to what we are trying to achieve with a Linux command. So, it's basically a normal console extended with Linux manual searching capability using natural language.

In essence, the setup is configured with :

- Input : Linux command + query strings on manual search mode.
- Output (hints) : switch(es) for that command to be run on console mode.

Please take a look at `usage <https://github.com/droyed/mansh/blob/main/README.rst#usage>`_ for a better picture.

Installation
------------

System requirements are Linux operating system and Python ``3.6`` or newer. Install dependencies from provided ``src/requirements.txt`` with pip or conda or manually one by one. 

Clone or unzip the downloaded zipped repository. Add ``.../src/`` to ``$PATH`` through your favourite shell config file (``.bashrc`` or ``.zshrc``, etc.) for permanently adding it. Make file named ``mansh`` executable with :

.. code-block:: console

    $ chmod +x mansh

Starting mansh
----------------
Run ``mansh`` shell with default argument values :

.. code-block:: console

    $ mansh

Explore all arguments :

.. code-block:: console

    $ mansh -h

With the default argument values, all instructions, key bindings and messages are printed on console with switch ``-info``. For detailed information on it, run :

.. code-block:: console

    $ mansh --infohelp

There's also "--vanish" argument to control vanishing messages at various stages. When this is input, vanishing messages is turned on. So, when we are fully comfortable with all instructions, key bindings and messages, we can *almost* switch off ``info`` values and start using ``mansh`` with something like :

.. code-block:: console

    $ mansh --info 000 --vanish

To go full hog on disabling messages, use : 

.. code-block:: console

    $ mansh --info 0000 --vanish

Usage
-----

Now, we are inside ``mansh`` shell. As mentioned earlier, ``mansh`` works as a two mode system - Normal console mode and Man-search mode. 

- Normal Console mode : Run linux commands and get output just like we would be on a normal console.

- Man-search mode is triggered by a tilde ``~`` at the start, followed by the linux command and then query string(s). The tilde is the differentiator between these two modes and that's how these two modes are accommodated into one shell. So, the general syntax is :

.. code-block:: console

    $ ~[command] [query string(s)]

``command`` is one among the available Linux commands. ``query string(s)`` are the query words based on which the semantic similarity search is performed across the man page for that Linux command.

Screencast
^^^^^^^^^^

Next up, some screencasts to show the usage in real-time with few Linux commands.

``convert`` has a huge collection of image-editing tools, but seems short on words in their manual pages and hence a good fit for ``mansh`` :
|gif_convert|

Here's with ``find`` to find certain types of files :
|gif_find|

With ``tree`` to list tree stucture in different ways :
|gif_tree|


**Note :** Your output would vary depending on - model type, delimiter and if there's any change in Linux man pages.


.. |Py-Versions| image:: https://img.shields.io/badge/Python-3.6+-blue
   :target: https://github.com/droyed/mansh

.. |OS| image:: https://img.shields.io/badge/Platform-%E2%98%AFLinux-9cf
   :target: https://github.com/droyed/mansh

.. |License| image:: https://img.shields.io/badge/license-MIT-green
   :target: https://raw.githubusercontent.com/droyed/mansh/master/LICENSE

.. |gif_tree| image:: https://github.com/droyed/mansh/blob/main/media/tree.gif
.. |gif_convert| image:: https://github.com/droyed/mansh/blob/main/media/convert.gif
.. |gif_find| image:: https://github.com/droyed/mansh/blob/main/media/find.gif