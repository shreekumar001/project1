import re,sys,socket,ssl

# Gather the parameters from commandline
numargv = len(sys.argv)
NUID = sys.argv[numargv-1]
host = sys.argv[numargv-2]

# Define the default port number and buffer size
# Default port will be used only if the user dont give the specific port number with SSL
# From requirements we know each package size will not beyond 256, so we set the buffer size to 256
port = 27993
buff = 256

# Define common socket and socket with SSL
s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sslsock = ssl.wrap_socket (s, ssl_version = ssl.PROTOCOL_TLSv1, ciphers = "AES256-SHA")

# Judge the command line parameters
if numargv > 3:

    if sys.argv[1] == "-p":
        try:
            port = int(sys.argv[2])
        except:
            sys.exit("Invalid Port NO")
        if sys.argv[3] == "-s":
            s = sslsock
    elif sys.argv[1] == "-s":
            port = 27994
            s = sslsock
    else:
        sys.exit("Parameters are wrong")

hellomsg = "cs5700spring2016 HELLO " + NUID + "\n"

# If the connection cannot be established, it will give back an error information
try:
    s.connect((host,port))
    s.send(hellomsg)

except:
    print("Cannot setup the link")
    sys.exit()

# Loop process the calculation. If the program detects the secret flag, it will jump from the loop
while True:
    try:
        revdata = s.recv(buff)
    except:
        sys.exit("Wrong connection information")
    try:
        sepdata = re.match (r"cs5700spring2016 STATUS ([0-9]*) (\W) ([0-9]*)",revdata)
        num1 = sepdata.group(1)
        operator = sepdata.group(2)
        num2 = sepdata.group(3)
        if int(num1) not in range (1,1001) or int(num2) not in range (1,1001):
            print "The numbers are not in range 1 to 1000"
            sys.exit()
    except:
        secret = revdata
        break

    # Calculate the result
    if operator == "+":
        ans = int(num1) + int(num2)
    if operator == "-":
        ans = int(num1) - int(num2)
    if operator == "*":
        ans = int(num1) * int(num2)
    if operator == "/":
        ans = int(num1) / int(num2)
    
    sendata = "cs5700spring2016 " + str(ans)+ "\n"
    s.send(sendata)

s.close()

# Grip the secret flag
flag = re.match (r"cs5700spring2016 (\w*) BYE",secret )
print flag.group(1)
