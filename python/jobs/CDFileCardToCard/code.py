# list_generators = ['tvli-erib0720' ]
list_generators = ['tvli-erib0720','tvli-erib0721','tvli-erib0722','tvli-erib0723','tvli-erib0724','tvli-erib0725','tvli-erib0726','tvli-erib0727','tvli-erib0728','tvli-erib0729','tvli-erib0730','tvli-erib0731']

def create_file(  list_generators,  path = '/opt/data/FilesForStubs'):
    for generator  in list_generators:
        with node(generator):
            from os import popen
            output=popen(f"""
                # if [[! -e /opt/data/FilesForStubs/CardToCardResponse.txt]];
                sudo mkdir -p {path}
                cd /opt/data/FilesForStubs/
                touch CardToCardResponse.txt
                # fi
                """).read()


def delete_folder(list_generators, path = '/opt/data/FileForStubs'):
    for generator  in list_generators:
        with node(generator):
            from os import popen
            output=popen(f"""sudo rm -r {path}""").read()




def wright_number(list_generators, number ,path = '/opt/data/FilesForStubs/CardToCardResponse.txt'):
    for generator  in list_generators:
        with node(generator):
            from os import popen
            output=popen(f"""echo {number} > {path}""").read()


if decision_list == 'create':
    print("1")
    create_file(list_generators)
elif decision_list == 'delete':
    print("2")
    delete_folder(list_generators)



print(numbers)

if numbers == 0 or numbers == 1:
    print("4")
    wright_number(list_generators, numbers)


print("3")



