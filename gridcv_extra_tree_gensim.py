from data_io import DataIO

import logging
from sklearn.decomposition import RandomizedPCA
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from pprint import pprint
from time import time
from sklearn.ensemble import ExtraTreesRegressor


dio = DataIO("Settings_loc5.json")

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


salaries = dio.get_salaries("train", log=True)

#title_corpus_csc = dio.read_gensim_corpus("train_title_nltk_filtered.corpus.mtx")
#desc_corpus_csc = dio.read_gensim_corpus("train_desc_nltk_filtered.corpus.mtx")
locraw_corpus_csc = dio.read_gensim_corpus("train_locraw_nltk_filtered.corpus.mtx")

#print title_corpus_csc.shape
print locraw_corpus_csc.shape


pipeline = Pipeline([
    ('pca', RandomizedPCA(random_state=3465343)),
    ('trees', ExtraTreesRegressor(min_samples_split=2, n_estimators=10,
                                  n_jobs=4)),
])

parameters = {
    'pca__n_components': range(100, 601, 100),
}

metric = dio.error_metric
if __name__ == "__main__":
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=1, verbose=3,
                               loss_func=metric,
                               iid=False,
                               refit=False)
    model_name = "ExtraTree_min_sample2_10trees_gridcv_desc_log"

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(locraw_corpus_csc, salaries)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_params_
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    best_estimator = pipeline.set_params(**best_parameters)
    dio.save_model(best_estimator, model_name, mae_cv=grid_search.best_score_, parameters="GridCV")
    print grid_search.cv_scores_
#title
#[CVScoreTuple(parameters={'pca__n_components': 50}, mean_validation_score=8114.354436894354, cv_validation_scores=array([ 7832.02927486,  8142.59464648,  8368.43938934])), CVScoreTuple(parameters={'pca__n_components': 100}, mean_validation_score=8050.372232184578, cv_validation_scores=array([ 7805.2436147 ,  8050.13238353,  8295.74069832])), CVScoreTuple(parameters={'pca__n_components': 150}, mean_validation_score=7992.0067620542031, cv_validation_scores=array([ 7713.16260219,  8011.95811042,  8250.89957355])), CVScoreTuple(parameters={'pca__n_components': 200}, mean_validation_score=7969.954716946886, cv_validation_scores=array([ 7686.53479712,  7994.52939814,  8228.79995559])), CVScoreTuple(parameters={'pca__n_components': 250}, mean_validation_score=7951.4574455230977, cv_validation_scores=array([ 7667.32401519,  7986.80421311,  8200.24410827])), CVScoreTuple(parameters={'pca__n_components': 300}, mean_validation_score=7944.4481204410049, cv_validation_scores=array([ 7679.24885978,  7956.03557116,  8198.05993038])), CVScoreTuple(parameters={'pca__n_components': 350}, mean_validation_score=7944.1183320537721, cv_validation_scores=array([ 7676.60423802,  7978.78605684,  8176.9647013 ])), CVScoreTuple(parameters={'pca__n_components': 400}, mean_validation_score=7899.1156367965059, cv_validation_scores=array([ 7645.1559318 ,  7910.82353156,  8141.36744703])), CVScoreTuple(parameters={'pca__n_components': 450}, mean_validation_score=7912.5157328026426, cv_validation_scores=array([ 7640.30124334,  7911.32395596,  8185.92199911])), CVScoreTuple(parameters={'pca__n_components': 500}, mean_validation_score=7895.2892790734322, cv_validation_scores=array([ 7605.04498066,  7907.65668509,  8173.16617146]))]
#Best score: 7895.289
#Best parameters set:
        #pca__n_components: 500

#description
#Best score: 9004.720
#Best parameters set:
        #pca__n_components: 200
#[CVScoreTuple(parameters={'pca__n_components': 100}, mean_validation_score=9030.5959214303093, cv_validation_scores=array([ 8729.14388367,  9085.7485522 ,  9276.89532842])), CVScoreTuple(parameters={'pca__n_components': 200}, mean_validation_score=9004.7195356220382, cv_validation_scores=array([ 8712.73164292,  9081.87764045,  9219.54932349])), CVScoreTuple(parameters={'pca__n_components': 300}, mean_validation_score=9064.9514615674289, cv_validation_scores=array([ 8783.89079244,  9134.31360085,  9276.64999141])), CVScoreTuple(parameters={'pca__n_components': 400}, mean_validation_score=9076.2734308900635, cv_validation_scores=array([ 8776.89542476,  9160.65547469,  9291.26939321])), CVScoreTuple(parameters={'pca__n_components': 500}, mean_validation_score=9135.1105593660341, cv_validation_scores=array([ 8850.89803432,  9207.27553593,  9347.15810784])), CVScoreTuple(parameters={'pca__n_components': 600}, mean_validation_score=9124.6361021371431, cv_validation_scores=array([ 8837.96896581,  9150.07743191,  9385.8619087 ]))]

#locraw
#Best score: 11682.736
#Best parameters set:
        #pca__n_components: 500
#[CVScoreTuple(parameters={'pca__n_components': 100}, mean_validation_score=11700.085554554107, cv_validation_scores=array([ 11406.18685298,  11712.73823257,  11981.33157811])), CVScoreTuple(parameters={'pca__n_components': 200}, mean_validation_score=11695.141211538628, cv_validation_scores=array([ 11397.00982221,  11709.27085742,  11979.14295498])), CVScoreTuple(parameters={'pca__n_components': 300}, mean_validation_score=11690.498230833402, cv_validation_scores=array([ 11396.93686941,  11711.90773147,  11962.65009162])), CVScoreTuple(parameters={'pca__n_components': 400}, mean_validation_score=11685.953107602816, cv_validation_scores=array([ 11393.0004248 ,  11698.86060978,  11965.99828823])), CVScoreTuple(parameters={'pca__n_components': 500}, mean_validation_score=11682.735588651414, cv_validation_scores=array([ 11393.70158166,  11697.70161791,  11956.80356639])), CVScoreTuple(parameters={'pca__n_components': 600}, mean_validation_score=11683.095522332193, cv_validation_scores=array([ 11387.12135864,  11698.48642768,  11963.67878067]))]
