
def getpof2(num):
    p=1
    while p < num:
        p*=2
    return p


def buildWalshTable(w,l, i1, i2, j1, j2, comp=False):
    if l == 2:
        if not comp:
            w[i1][j1] = 1
            w[i1][j2] = 1
            w[i2][j1] = 1
            w[i2][j2] = -1
        else:
            w[i1][j1] = -1
            w[i1][j2] = -1
            w[i2][j1] = -1
            w[i2][j2] = 1
        return
    midi = (i1 + i2) // 2
    midj = (j1 + j2) // 2
    buildWalshTable(w,l/2, i1, midi, j1, midj,comp)
    buildWalshTable(w,l/2, i1, midi, midj + 1, j2,comp)
    buildWalshTable(w,l/2, midi + 1, i2, j1, midj,comp)
    buildWalshTable(w,l/2, midi + 1, i2, midj + 1, j2,not comp)
    return


if __name__ =='__main__':
    w=[[0 for i in range(2)] for j in range(2)]
    buildWalshTable(w,2,0,1,0,1)
    print(w)
