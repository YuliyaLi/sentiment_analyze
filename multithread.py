
import threading
from sentiment_grg import Struct, Score
import pandas as pd
import numpy as np




class Content():
    def __init__(self):
        pass
    def multiscore(self, score, log_pandas, thread_id):
        #score.getscore(text)
    #def sensitive_words(self, find, log_pandas, stop_words, thread_id):
        log_conversation_list = np.array(log_pandas['CONVERSATION']).tolist()
        log_id_list = np.array(log_pandas['CALL_ID']).tolist()

        log_dict = {}
        log_temp = []
        for i in range(len(log_id_list)):
            if (log_id_list[i] not in log_temp):
                log_temp.append(log_id_list[i])
                log_dict[log_id_list[i]] = log_conversation_list[i]
            else:
                log_dict[log_id_list[i]] = log_dict[log_id_list[i]] + log_conversation_list[i]
        content_dict = {}

        # 获取文本中text,返回分数
        #score.getscore(text)
        for key in log_dict.keys():
            result = score.getscore(log_dict[key])
            #neg_words = find.match(log_dict[key])
            #neg_words = stop_words.remove_stop_words(neg_words)
            #key + '_score=%d; word=%s; nor_word=%s; degree_word=%s;' % (score, score_words, not_word, degree_word))
            content_dict[key] = result
            #"degree_word="+result.degree_word+ ";not_word=" + result.not_word+ ";score_words="+result.score_words
        content_pandas = pd.Series(content_dict)
        path = "result/result" + str(thread_id) + ".csv"
        content_pandas.to_csv(path)
        return content_pandas



    pass



if __name__=='__main__':
    sentiment_dict_path = "./sentiment_words_chinese.tsv"  #/sentiment_words_chinese.tsv
    degree_dict_path = "./degree_dict.txt"
    text_path = "chatLog.csv"
    score = Score(sentiment_dict_path, degree_dict_path )
    log_pandas = pd.read_csv(text_path, encoding="gbk")
    cont = Content()

    lock = threading.Lock()

    for x in range(100):
        # t = threading.Thread(target = cont.content,args =(find_neg,find_pos,log_pandas,stop_words,x))
        lock.acquire()
        t = threading.Thread(target=cont.multiscore,  #多个同时计算
                             args=(score, log_pandas, x))  # cont.getscore需要的参数：词典，文本，线程id
        t.start()
        lock.release()
    print("Main Thread End")
    #text = "今天超级糟报" #"我今天很(不)开心"


    pass
