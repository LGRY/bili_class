#coding:utf-8
from keras.preprocessing.text import Tokenizer #建立字典
from keras.preprocessing import sequence #统一化维度
import os

def readfeed():
    feedlist = []
    #读取负面新闻
    for i in os.listdir('train/neg'):
        with open('train/neg/'+i,'r') as r:
            res = r.readline()
            feedlist.append(res)
    # 读取正面新闻
    for i in os.listdir('train/pos'):
        with open('train/pos/'+i,'r') as r:
            res = r.readline()
            feedlist.append(res)
    print len(feedlist)
    return feedlist

#建立一个2000个单词的字典（top频率出现的）
token = Tokenizer(num_words=2000)
#读取所有训练集，按照单词出现频次，构成字典
word = readfeed()
# 读取所有训练集，按单词出现的频数排序，构成字典
token.fit_on_texts(word)
#打印一共有多少个文档
print token.document_count
#打印每个单词出现的次数
# print  token.word_counts
#查看映射关系
print token.word_index
exit()
#实际单词转成数字映射关系放在列表
x_train_seq = token.texts_to_sequences(word) #[a:1 b:2 cc:3]
#这里只打印单词的映射数字
# print x_train_seq[10]


#通过pad seq功能统一每一段文字文字shape 如果大于100 从前边干掉，如果小于100 前边为0  可以设定pad方式 paddingding=pre post
x_train =  sequence.pad_sequences(x_train_seq,maxlen=200,padding='post')
all_lable = [1] * 12500 + [0] * 12500
# print x_train

#--------------------
from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation,Flatten
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import SimpleRNN

model=Sequential()
model.add(Embedding(
    output_dim=32,
    input_dim=2000,
    input_length=200)
         )
model.add(
    Dropout(0.1)
         )
model.add(
    SimpleRNN(units=16)
         )
model.add(
    Dense(units=256,
          activation='relu')
         )
model.add(
    Dropout(0.1)
         )

model.add(Dense(units=1,
                activation='sigmoid'
                )
          )

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.fit(
    x=x_train,
    y=all_lable,
    batch_size=500,
    validation_split=0.2,
    epochs=10
)
model.save('text.h5')





#什么是词向量?embedding
# ”词向量”（词嵌入）是将一类将词的语义映射到向量空间中去的自然语言处理技术。即将一个词用特定的向量来表示，向量之间的距离
# （例如，任意两个向量之间的L2范式距离或更常用的余弦距离）一定程度上表征了的词之间的语义关系。由这些向量形成的几何空间被称为一个嵌入空间。
#
# 例如，“椰子”和“北极熊”是语义上完全不同的词，所以它们的词向量在一个合理的嵌入空间的距离将会非常遥远。但“厨房”和“晚餐”是相关
# 的话，所以它们的词向量之间的距离会相对小。
#
# 理想的情况下，在一个良好的嵌入空间里，从“厨房”向量到“晚餐”向量的“路径”向量会精确地捕捉这两个概念之间的语义关系。在这种情况下，
# “路径”向量表示的是“发生的地点”，所以你会期望“厨房”向量 - “晚餐"向量（两个词向量的差异）捕捉到“发生的地点”这样的语义关系。基本上，
# 我们应该有向量等式：晚餐 + 发生的地点 = 厨房（至少接近）。如果真的是这样的话，那么我们可以使用这样的关系向量来回答某些问题。例如，
# 应用这种语义关系到一个新的向量，比如“工作”，我们应该得到一个有意义的等式，工作+ 发生的地点 = 办公室，来回答“工作发生在哪里？”。
#
# 词向量通过降维技术表征文本数据集中的词的共现信息。方法包括神经网络(“Word2vec”技术)，或矩阵分解。