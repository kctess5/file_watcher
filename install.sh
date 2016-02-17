#!/bin/bash

# find watch file
export FILE_WATCHER=$(pwd)/watch.py

# attempt to find bash profile
bash_profile="~/"
if [ -f ~/.bashrc ]; then 
	bash_profile="~/.bashrc"
elif [ -f ~/.bash_profile ]; then 
	bash_profile="~/.bash_profile"
elif [ -f ~/.profile ]; then 
	bash_profile="~/.profile"
fi

read -p "Enter path to bash profile: (default: $bash_profile): " -e profile_actual
[ -z "${profile_actual}" ] && profile_actual=$bash_profile

# expand profile path
profile_actual="${profile_actual/#\~/$HOME}"

echo "Appending wrapper function to: $profile_actual"
echo "function watch()  { python $FILE_WATCHER \"\$@\"; }" >> $profile_actual