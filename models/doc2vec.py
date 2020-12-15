import json
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open(ProjectPath + '/data/fund_date.json', 'r') as fp:
    fund_data = json.load(fp)
fund_data_dict = {}
for fund in fund_data:
    fund_data_dict[fund['fund_id']] = {**fund}


def read_navs(fund_data):
    fund_nav = {}
    for fund in fund_data:
        navs = list()
        for _nav in fund['nav']:
            navs.append('{:.4f}'.format(_nav['unit_net_value']))
        fund_nav[fund['fund_id']] = navs
        # fund_nav.append(TaggedDocument(navs, tags=[fund['fund_id']]))
    return fund_nav


def nav2corpus(fund_nav):
    train_docs = []
    for f_id, navs in fund_nav.items():
        train_docs.append(TaggedDocument(navs, tags=[f_id]))
    return train_docs


def train_model(train_docs):
    model = Doc2Vec(train_docs, vector_size=100, sample=1e-6, workers=4)
    model.train(train_docs, total_examples=model.corpus_count, epochs=100)
    print('模型训练完成，开始保存')
    model.save('../pkcgs/time2vec.model')


def test_model(f_id, navs):
    model = Doc2Vec.load('../pkcgs/time2vec.model')
    inferred_vector_dm = model.infer_vector(navs)
    sims = model.docvecs.most_similar([inferred_vector_dm])
    print('{}:{} 相似度前十的基金'.format(f_id, fund_data_dict[f_id]['symbol']))
    for _id, sim in sims:
        print('{}:{} 相似度={:.4f}'.format(_id, fund_data_dict[_id]['symbol'], sim))
    print()


if __name__ == '__main__':
    fund_nav = read_navs(fund_data)
    # _corpus = nav2corpus(fund_nav)
    # train_model(_corpus)
    test_model('005911', fund_nav['005911'])
