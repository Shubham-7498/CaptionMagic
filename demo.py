def count_sequences(r,g,b,prev,memory):
    if(r,g,b,prev) in memory:
        return memory[(r,g,b,prev)]

    if r==0 and g==0 and b==0 :
        return 1
    
    total=0
    
    if r>0 and prev!="R":
        total+=count_sequences(r-1,g,b,"R",memory)
    if g>0 and prev!="G":
        total+=count_sequences(r,g-1,b,"G",memory)
    if b>0 and prev!="B":
        total+=count_sequences(r,g,b-1,"B",memory)

    memory[(r,g,b,prev)] = total
    return total

R,G,B = map(int,input("Enter R,G,B:").split())

memory={}

result=count_sequences(R,G,B,"", memory)

print(result)

