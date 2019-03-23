Vue.config.devtools = true;

onload = function() {

  const app = new Vue({
      el: '#app',
      data: {
        items: plot_data,
        pca_vec: dist_2vec(),
        videoId_map: videoId_map,
        song_list: [],
        singer_list: ['YuNi'],
        selected_video_id: ""
      },
      methods: {
        getSearchResult: function(){
          result = []

          is_and_search = document.getElementById("search-type").group1[0].checked
          console.log(is_and_search)

          if(is_and_search){
            
            first_singer_song_list = []
            singer = this.singer_list[0]
            for(song in this.videoId_map[singer]){
              first_singer_song_list.push(song)
            }

            for(var i = 0; i < first_singer_song_list.length; i++){
              song = first_singer_song_list[i]
              will_append = true
              for(var j = 0; j < this.singer_list.length; j++){
                singer = this.singer_list[j]
                if(!this.videoId_map[singer][song]){
                  will_append = false
                  break
                }
              }

              if(will_append){
                for(var j = 0; j < this.singer_list.length; j++){
                  singer = this.singer_list[j]
                  result.push({singer: singer, song: song, video_id: videoId_map[singer][song]})
                }
              }
            }
          }else
          {
            for(var i = 0; i < this.singer_list.length; i++){  
              singer = this.singer_list[i]
              for(song in this.videoId_map[singer]){
                result.push({singer: singer, song: song, video_id: videoId_map[singer][song]})
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
        }
      }
    })

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

function dist_2vec(){
    vectors = PCA.getEigenVectors(dist_mat)

    pos_list = new Array(vectors[0]["vector"].length)
    xSum = 0
    ySum = 0
    for(var i = 0; i < vectors[0]["vector"].length; i++){
      pos_list[i] = [-vectors[0]["vector"][i], vectors[1]["vector"][i]]
      xSum += (-vectors[0]["vector"][i])
      ySum += (vectors[1]["vector"][i])
    }
    xAve = xSum/pos_list.length
    yAve = ySum/pos_list.length

    xMax = 0
    yMax = 0
    for(var i = 0; i < vectors[0]["vector"].length; i++){
      pos_list[i][0] -= xAve
      pos_list[i][1] -= yAve

      if (xMax < pos_list[i][0]){
        xMax = Math.abs(pos_list[i][0])
      }

      if (yMax < Math.abs(pos_list[i][1])){
        yMax = Math.abs(pos_list[i][1])
      }
    }

    xScale = 0.95/xMax
    yScale = 0.95/yMax

    for(var i = 0; i < pos_list.length; i++){
      pos_list[i][0] *= xScale
      pos_list[i][1] *= yScale
    }

    return pos_list
}
