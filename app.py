import flask
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from joblib import dump, load

app = flask.Flask( __name__, template_folder='templates' )

model_df = load( './model/df.joblib' )
model = load( './model/player_index_with_neighbours.joblib' )

def recommend_me(player):
    player = player.title()
    recomend_name=[]
    index = model_df[model_df['Name']== player].index.tolist()[0]
    for i in model[index][1:]:
        recomend_name.append(model_df.iloc[i]['Name'])
    return recomend_name
        # print(data1.iloc[i]['Photo'])


all_p_name = []
name_df = model_df['Name']
for i in name_df:
    all_p_name.append( i.lower() )


# Set up the main route
@app.route( '/', methods=['GET', 'POST'] )
def main():
    if flask.request.method == 'GET':
        return flask.render_template( 'index.html' )

    if flask.request.method == 'POST':
        p_name = flask.request.form['player_name']
        # p_name = p_name.title()
        p_name = p_name.lower()
        if p_name not in all_p_name:
            return flask.render_template( 'negative.html', pName=p_name )
        else:
            result_final = recommend_me( p_name )

            return flask.render_template( 'positive.html', player_name=result_final, search_name=p_name.title())


if __name__ == '__main__':
    app.run()
