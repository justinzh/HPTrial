from csv import reader, writer, QUOTE_ALL

skips = ['===>', '____', 'F3=E', 'UPDA', ]
cnt = 0
refs = {}

csvfile =  open('data_parsed.csv', 'w', newline='')
writer = writer(csvfile, quoting=QUOTE_ALL)
writer.writerow(['no', 'code', 'description', 'function', 'authorization'])

with open('data.csv', 'r') as read_obj:
    try:
        print('starting...')
        csv_reader = reader(read_obj)
        for words in csv_reader:
            cnt += 1
            # remove empty fields
            words = list(filter(lambda x: len(x.strip())!= 0, words))
            
            # skip irrelevant lines            
            if words[0][:4] in skips:
                continue
            
            rl = len(words)

            # extract code and description
            if words[0] == 'RUN DATE:':
                code  = -9999
                print(code)
                continue
            if code == -9999:
                code = words[1]
                description = words[2]

                bRefs = True
                bLog = False

                print('code: %s, desc: %s' % (code, description))
                continue

            if bRefs:
                if rl == 1 or rl == 3:
                    si = words[rl-1].find(' ')
                    if words[rl-1][:si].isnumeric():
                        refs[words[rl-1][:si]] = words[rl-1][si+1:]
                if rl >= 2: 
                    refs[words[0]] = words[1]
                print(refs)

            # extracting logs
            if words[0] == 'Selection or command':
                bRefs = False
                bLog = True
                continue

            # out put result here....
            if bLog:
                if words[0].isnumeric():
                    no =  words[0]
                    print('no:%s' % no)
                    continue

                if words[0][:4]=='AUTH':       
                    line = ' '.join(words)
                    line=line[line.find(' ')+1:]
                    permissions = line.split(' ')

                    print('merged line:%s' % line)
                    print(permissions)

                    for permission in permissions:
                        writer.writerow([no, code, description, refs[no], permission])
    except Exception as ex:
        print('Exception on row# %d' % cnt)
        print(words)
        print(ex)
    else:
        print('Completed with on error: %d lines were read:' % cnt)

    csvfile.close()