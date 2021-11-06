import socket
import csv

# open connection
PORT_NUM = 5000
size = 1024
try: #socket creation
    socket_def = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_def.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #print the socket with the wrong number
    socket_def.bind(('', PORT_NUM))
    socket_def.listen(1)
    print('Connect to server with port number=', PORT_NUM)

    #in case there is an error

except socket.error as e:
    print("error")

# create two files [sortByName,sortByPrice] in which they aims to sort 'smartphones.csv' according to name and price respectively
file = 'smartphones.csv'
sortByName = open('sortByName', 'w')
sortByPrice = open('sortByPrice', 'w')
#open the file
reader = csv.reader(open(file), delimiter=",")
#just to ignore the name and the price
next(reader)
#sort by name and price
names = sorted(reader, key=lambda row: row[0], reverse=False)
reader = csv.reader(open(file), delimiter=",")
next(reader)
price = sorted(reader, key=lambda row: row[1], reverse=False)
#open file and print data on it
with open('sortByName', 'w') as f:
    for item in names:
        f.write("%s\n" % item)
with open('sortByPrice', 'w') as f:
    for item in price:
        f.write("%s\n" % item)
# print(names)
# print(price)
sortByName.close()
sortByPrice.close()


def request_wrong():
    global response
    #creats an html file and print the error
    response = '<html><head><title>Error</title></head><body><p style="color:red">The file is not found</p><br><p><b>&nbsp;&nbsp;&nbsp;&nbsp;Mayar Abuzahra            1181239</b></p><br><br><p><b>&nbsp;&nbsp;&nbsp;&nbsp;Shahed Jamhour            1180654</b></p><br><br><p><b>&nbsp;&nbsp;&nbsp;&nbsp;Yasmeena Assi             1180899</b></p><br><br></body></html>'.encode(
        'utf-8')
    response += ("IP=" + str(ip) + " Port=" + str(port)).encode()

while (1):
    #create connection
      connection,address = socket_def.accept()  #Accept connection with client side
      ip = address[0]
      port = address[1]
      addr=(ip,port)
      print(f"New connection {addr} connected.")
      FileNameRequest = connection.recv(size).decode('utf-8')
      if not FileNameRequest:
            # if data is not received break
       break
      print(f"[Client request]:")
      requestAfterSplitting = FileNameRequest.split()  # Split request from spaces
      request_file = requestAfterSplitting[1]
      ef = request_file.split('?')
      extFile=ef[0]
      extFile = extFile.strip('/')

      if (extFile== '' or extFile=="main.html"):
           extFile = 'main.html'  
      elif (extFile[5:] == ".css"):
           extFile = 'style.css'
      elif (extFile== "file.html"):
           extFile = 'file.html'

      try:
         file = open(extFile, 'rb')
         response = file.read()
         file.close()

         if (extFile[7:]==".png"):
                ft = 'Capture.png'
         elif (extFile[7:]==".jpg"):
                ft = 'Picture.jpg'
         elif (extFile.endswith(".csv")):
                ft = file
         else:
                ft = ''

         header_line ='HTTP/1.1 200 OK\n'+ 'Content-Type: ' + str(ft) + '\n\n'
         print(header_line)

      except Exception as exp:
        header_line = 'HTTP/1.1 404 Not Found\n\n'
        print(header_line)
        request_wrong()

      last_res = header_line.encode('utf-8')
      last_res += response  # add response message to header response
      connection.send(last_res)  # send the server response
      connection.close()  # close the connection of client
