semantic_thr = 0.7



semantic_model_name = 'cointegrated/rubert-tiny2'
semantic_model_path = 'cointegrated/rubert-tiny2' # 'best_75_enc.pt'

clickbait_model_name = 'cointegrated/rubert-tiny2'
clickbait_model_path = 'cointegrated/rubert-tiny2' # 'best_75_enc.pt'

ner_model_name = 'surdan/LaBSE_ner_nerel'

device = 'cpu'


NER_CONTENT = 'ner_content'
SEMANTIC = 'semantic'
CLICKBAIT = 'clickbait'
SOURCES = 'sources'
STATUS = 'status'
SCORE = 'score'
CONTENT = 'content'
SUCCESS = 'success'
RESPONSE = 'response'
RESULT = 'result'
NOT_FOUND = 'not found'
NO_PRIMARY = 'no primary'
WITH_PRIMARY = 'with primary'
NER_INTER = 'ner_inter'
NER_ADD = 'ner_add'
DATE = 'date'
NAME = 'name'
TITLE = 'title'