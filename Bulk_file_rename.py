import os

def main():
    i=0
    path=input("Enter path: ")
    file_name=input("Enter file name:")
    file_format=input("Enter file format (eg: .jpg): ")

    for filename in os.listdir(path):
        my_dest=file_name+str(i)+file_format
        my_source=path+filename
        my_dest=path+my_dest
        os.rename(my_source,my_dest)
        i+=1

if __name__ == '___main__':
    main()