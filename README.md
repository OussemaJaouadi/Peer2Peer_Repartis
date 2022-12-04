# Project Repartis : 

:books: A peer to peer file sharing network that implements a protocol similar to the bitTorrent network. :books:

## Usage :

In order to run this code, one only needs to run the command `python3 $(pwd)/src/CLI.py`.
This will start the command line interface for the software.

The program will prompt for users to enter the path for the directory they wish to initialize their shared directory in.
The user may enter an *absolute or relative path* for this prompt.

Once the program initializes, any files can be added to the users shared folder and they will be added to the network.

**_Note:_** Python 3.6 or above is required

## App architecture : 

> ### CLI.py : main app
> Developped with interactive User experience
> ### utils : package made for recyclable needed functions
>   * [artist](./src/utils/artist.py) : util generating the ascii art of console 
>   * [UI_colors](./src/utils/UI_colors.py) : shell colors to make the interacion between user and terminal easier
>   * [proress_bar](./src/utils/progress_bar.py) : an interactive progress bar for user
>   * [SpinnerThread](./src/utils/SpinnerThread.py) : a spinner for the user to show while he is waiting
>   * [files](./src/utils/files.py) : FileReader and DirectoryReader classes


## References : 

> [FileFunctions](http://bdurblg.blogspot.com/2011/06/python-split-any-file-binary-to.html) <br>
> [HashFuntion](https://stackoverflow.com/questions/22058048/hashing-a-file-in-python) <br>
> [ShellColors](https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal) <br>
> [Spinner](https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal) <br>
> 

## Authors :rocket:

* **Oussema Jaouadi**
* **Taha Mediouni**

**Enjoy :sunglasses:**

