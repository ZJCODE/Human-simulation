import numpy as np
 
def alias_setup(probs):
    '''
    probs： 某个概率分布
    返回: Alias数组与Prob数组
    '''
    K       = len(probs)
    q       = np.zeros(K) # 对应Prob数组
    J       = np.zeros(K, dtype=np.int) # 对应Alias数组
    # Sort the data into the outcomes with probabilities
    # that are larger and smaller than 1/K.
    smaller = [] # 存储比1小的列
    larger  = [] # 存储比1大的列
    for kk, prob in enumerate(probs):
        q[kk] = K*prob # 概率
        if q[kk] < 1.0:
            smaller.append(kk)
        else:
            larger.append(kk)
 
    # Loop though and create little binary mixtures that
    # appropriately allocate the larger outcomes over the
    # overall uniform mixture.
    
    # 通过拼凑，将各个类别都凑为1

    while len(smaller) > 0 and len(larger) > 0:
        small = smaller.pop()
        large = larger.pop()

        J[small] = large # 填充Alias数组
        q[large] = q[large] - (1.0 - q[small]) # 将大的分到小的上
        
        if q[large] < 1.0:
            smaller.append(large)
        elif q[large] > 1.0:
            larger.append(large)
        else:
            pass
    return J, q
 
def alias_draw(J, q):
    '''
    输入: Prob数组和Alias数组
    输出: 一次采样结果
    '''
    K  = len(J)
    # Draw from the overall uniform mixture.
    kk = int(np.floor(np.random.rand()*K)) # 随机取一列
 
    # Draw from the binary mixture, either keeping the
    # small one, or choosing the associated larger one.
    if np.random.rand() < q[kk]: # 比较
        return kk
    else:
        return J[kk]

def sampling(distribution):
	J, q = alias_setup(distribution)
	return alias_draw(J, q)


def get_color():
    color_list = ['b','g','r','c','m','y','k','w']
    while True:     
        for c in color_list:
            yield c


if __name__ == '__main__':

	distribution = [0.2,0.2,0.1,0.5]
	s = sampling(distribution)
	print(s)


