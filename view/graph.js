Vue.config.devtools = true;

onload = function() {

    const app = new Vue({
        el: '#app',
        data: {
          items: plot_data,
          pca_vec_all: [],
          videoId_map: videoId_map,
          song_list: [],
          singer_list: ['YuNi'],
          selected_video_id: ""
        },
        methods: {
          getSearchResult: function(){
            result = []

            search_threashold = 0
            if(document.getElementById("search-type").group1[0].checked){
              search_threashold = this.singer_list.length/1;
            }else if(document.getElementById("search-type").group1[1].checked){
              search_threashold = this.singer_list.length/2
            }else if(document.getElementById("search-type").group1[2].checked){
              search_threashold = this.singer_list.length/4
            }else{
              search_threashold = this.singer_list.length/this.singer_list.length;
            }

            console.log(search_threashold)
            song_singer_map = {}
            for(var i = 0; i < this.singer_list.length; i++){
              singer = this.singer_list[i]
              for(song in this.videoId_map[singer]){
                if(!song_singer_map[song]){
                  song_singer_map[song] = []
                }
                song_singer_map[song].push(singer)
              }
            }

            for(song in song_singer_map){
              if(song_singer_map[song].length >= search_threashold){
                for(var j = 0; j < song_singer_map[song].length; j++){
                  singer = song_singer_map[song][j]
                  result.push({singer: singer, song: song, video_id: videoId_map[singer][song], popularity: song_singer_map[song].length*100.0/this.singer_list.length})
                }
              }
            }
            return result
          },
          isSinging(singer){
            if(this.singer_list.indexOf(singer) > -1){
              return true
            }

            for(so in this.videoId_map[singer]){
              if(this.song_list.indexOf(so) > -1){
                return true
              }
            }
  
            return false
          },
          dist2vec(singer_list){
            // singer_listが0だったら全員分やる
            console.log(singer_list)
            var singer_list_tmp = []
            if(singer_list.length == 0){
              for(var i = 0; i < plot_data.length; i++){
                  singer_list_tmp.push(plot_data[i].name)
              }
            }

            // singer_listが1だったら選曲傾向とかないので0, 0で戻す
            if(singer_list.length == 1){
              return [{singer: singer_list[0], posX: 0, posY: 0}]
            }

            // singer_listが2だったら正規化したあとの距離1なの確定なので1, 1と-1, -1で戻す
            if(singer_list.length == 2){
              return [{singer: singer_list[0], posX: 0.9, posY: 0.9}, {singer: singer_list[1], posX: -0.9, posY: -0.9}]
            }

            // それ以上だったらちゃんと計算する
            for(var i = 0; i < singer_list.length; i++){
              singer_list_tmp.push(singer_list[i])
            }

            singer_id_list = []
            for(var i = 0; i < plot_data.length; i++){
              if(singer_list_tmp.indexOf(plot_data[i].name) > -1){
                singer_id_list.push(plot_data[i].singer_id)
              }
            }

            var dist_mat_calc = []
            for(var i = 0; i < singer_id_list.length; i++){
              dist_mat_row = []
              for(var j = 0; j < singer_id_list.length; j++){
                dist_mat_row.push(dist_mat[singer_id_list[i]][singer_id_list[j]])
              }
              dist_mat_calc.push(dist_mat_row)
            }

            console.log(dist_mat_calc)
            vectors = PCA.getEigenVectors(dist_mat_calc)

            pos_list = new Array(vectors[0]["vector"].length)
            xSum = 0
            ySum = 0
            for(var i = 0; i < vectors[0]["vector"].length; i++){
              pos_list[i] = [-vectors[0]["vector"][i], vectors[1]["vector"][i]]
              xSum += pos_list[i][0]
              ySum += pos_list[i][1]
            }
            xAve = xSum/pos_list.length
            yAve = ySum/pos_list.length
        
            xMax = 0
            yMax = 0
            for(var i = 0; i < vectors[0]["vector"].length; i++){
              pos_list[i][0] -= xAve
              pos_list[i][1] -= yAve
        
              if (xMax < Math.abs(pos_list[i][0])){
                xMax = Math.abs(pos_list[i][0])
              }
        
              if (yMax < Math.abs(pos_list[i][1])){
                yMax = Math.abs(pos_list[i][1])
              }
            }
        
            xScale = 0.9/xMax
            yScale = 0.9/yMax
        
            for(var i = 0; i < pos_list.length; i++){
              pos_list[i][0] *= xScale
              pos_list[i][1] *= yScale
            }
            
            result = []
            console.log(pos_list)
            for(var i = 0; i < singer_list_tmp.length; i++){
              result.push({singer: singer_list_tmp[i], posX: pos_list[i][0], posY: pos_list[i][1]})
            }

            return result
          }
        }
    })

    app.pca_vec_all = app.dist2vec([])

    var elems = document.querySelectorAll('.chips')
    var all_singer_list = []
    for(var i = 0; i < plot_data.length; i++){
      all_singer_list.push(plot_data[i]["name"])
    }

    singer_autocomplete = {}
    for(var i = 0; i < all_singer_list.length; i++){
      singer_autocomplete[all_singer_list[i]] = null
    }

    var instances = M.Chips.init(elems, {
      data : [
        {tag: 'YuNi'}
      ],
      placeholder: 'Vsinger',
      secondaryPlaceholder: '+Vsinger',
      autocompleteOptions: {
        data: singer_autocomplete,
        limit: Infinity,
        minLength: 1
      },
      onChipAdd: function(){
        app.singer_list.push(this.chipsData[this.chipsData.length - 1]["tag"])
      },
      onChipDelete: function(){
        existing_tags = []
        for(var i = 0; i < this.chipsData.length; i++){
          existing_tags.push(this.chipsData[i]["tag"])
        }

        for(var i = app.singer_list.length; i >= 0; i--){
          if(existing_tags.indexOf(app.singer_list[i]) == -1){
            app.singer_list.splice(i, 1)
          }
        }
      }
    })
};