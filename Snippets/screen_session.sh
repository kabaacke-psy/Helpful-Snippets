# https://linuxize.com/post/how-to-use-linux-screen/

# The screen command allows you to save your progress in a  remotete session when accessing the cluster via SSH

# To start a screen session, enter the following command in the remote terminal window. It helps to name the session using the -S flag followed by the name you want to give your session

screen -S {SESSION_NAME}

# Now, when you disconnect from your SSH session, your place will be kept and the session you were running will stay up.

# When you log back in, you can check whch screen sessions for your account are active by using the following command

screen -ls

# To resume a previous screen session, use the following command, followed by the identifier of the screen session

screen -r {SESSION_NAME}

# You can also kill a detached screen session using the following command

screen -X -S {SESSION_NAME} kill

# If the screen session says that it is attached, but you are not connected to it, you can detach it using the -d option

screen -d {SESSION_NAME}

# To directly connect to a screen session that is attached to another terminal, you can use both the -r and the -d flags.

screen -r -d {SESSION_NAME}

