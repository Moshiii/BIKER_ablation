import pandas as pd

# import os
# print(os.getcwd())


def main():

    df_result = pd.read_csv(
        "result\BIKER_3_sampling_from_training_testing_result.csv")

    print(list(df_result))
    records = df_result.to_records(index=False)
    # print(records[:2])
    result_list = []
    count = 0

    main.mrr = 0.0
    main.map = 0.0
    main.tot = 0

    main.total_Bi_Encoder_precision=[0]*4
    main.total_Bi_Encoder_recall=[0]*4

    for x in records:
        # compute_stats_original(x)
        compute_stats(x)

    print(main.mrr/len(records),main.map/len(records))

def compute_stats_original(x):

    hit_position = x[1]
    query = x[2]
    true_apis = eval(x[3])
    top_questions = eval(x[4])
    recommended_api = eval(x[5])
    # print(true_apis)
    
    # print(recommended_api)

    pos = -1
    tmp_map = 0.0
    hits = 0.0
    
    for i, api in enumerate(recommended_api):
        if api in true_apis and pos == -1:
            pos = i+1
        if api in true_apis:
            hits += 1
            tmp_map += hits/(i+1)
    tmp_map /= len(true_apis)
    tmp_mrr = 0.0
    if pos != -1:
        tmp_mrr = 1.0/pos

    main.map += tmp_map
    main.mrr += tmp_mrr

    # print(tmp_mrr, tmp_map, pos, query, true_apis, len(recommended_api))


def compute_stats(x):


    hit_position = x[1]
    query = x[2]
    true_apis = eval(x[3])
    top_questions = eval(x[4])
    recommended_api = eval(x[5])

    top_k= len(recommended_api)
    
    Bi_Encoder_hit_list=[0]*top_k
    Bi_Encoder_hit_recall_list=[0]*top_k
    
    pos = -1
    tmp_map = 0.0
    hits = 0.0
    temp_true_apis=list(true_apis)
    
    len_api=len(temp_true_apis)
    for i,api in enumerate(recommended_api):
        if api in true_apis:
            Bi_Encoder_hit_list[i]=1
        if api in true_apis and pos == -1:
            pos = i+1
        if api in temp_true_apis:
            hits += 1
            Bi_Encoder_hit_recall_list[i]=1
            tmp_map += hits/(i+1)
            temp_true_apis.remove(api)
    tmp_map /= len(true_apis)
    tmp_mrr = 0.0
    if pos!=-1:
        tmp_mrr = 1.0/pos
    
    temp_precision=[0]*4
    temp_recall=[0]*4

    # print(true_apis)
    # print(recommended_api)
    # print(tmp_mrr, tmp_map, pos, query, true_apis, len(recommended_api))

    for idx, n in enumerate([1,3,5,10]):
    # print(Bi_Encoder_hit_recall_list)
        temp_precision[idx] = sum(Bi_Encoder_hit_list[:n])/n
        temp_recall[idx] = sum(Bi_Encoder_hit_recall_list[:n])/(len_api)

    main.total_Bi_Encoder_precision = [x + y for (x, y) in zip(main.total_Bi_Encoder_precision, temp_precision)]
    
    main.total_Bi_Encoder_recall = [x + y for (x, y) in zip(main.total_Bi_Encoder_recall, temp_recall)]
    
    # print(main.total_Bi_Encoder_precision)
    # print(main.total_Bi_Encoder_recall)

    main.map += tmp_map
    main.mrr += tmp_mrr

    # print(tmp_mrr, tmp_map, pos, query, true_apis, len(recommended_api))



if __name__ == "__main__":
    main()
