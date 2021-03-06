Vue.config.devtools = true;

onload = function() {
    const app = new Vue({
        el: '#app',
        data: {
            videoId_map: videoId_map,
            singer_id: 0,
            song_id: 0,
            width: window.innerWidth,
            height: window.innerHeight
        },
        methods: {
            getYAxisSong: function(){
                videoId_list = []
                
                //first and second element
                singer_name = plot_data[this.singer_id].name
                song_name = song_list[this.song_id]

                for(var i = this.song_id - 1; i >= 0; i--){
                    if(Object.keys(videoId_map[singer_name]).includes(song_list[i])){
                        videoId_list.push(videoId_map[singer_name][song_list[i]])
                        break
                    }
                }
                if(videoId_list.length == 0){
                    videoId_list.push("")
                }

                videoId_list.push("")

                for(var i = this.song_id + 1; i < song_list.length; i++){
                    if(Object.keys(videoId_map[singer_name]).includes(song_list[i])){
                        videoId_list.push(videoId_map[singer_name][song_list[i]])
                    }
            }
            console.log(videoId_list)
            return videoId_list

            },
            getXAxisSong: function(){
                videoId_list = []

                singer_name = plot_data[this.singer_id].name
                song_name = song_list[this.song_id]
                
                //first element
                for(var i = this.singer_id - 1; i >= 0; i--){
                    test_singer_name = plot_data[i].name
                    if(Object.keys(videoId_map[test_singer_name]).includes(song_name)){
                        videoId_list.push(videoId_map[test_singer_name][song_name])
                        break
                    }
                }
                if(videoId_list.length == 0){
                    videoId_list.push("")
                }

                videoId_list.push("")

                for(var i = this.singer_id + 1; i < plot_data.length; i++){
                    test_singer_name = plot_data[i].name
                    if(Object.keys(videoId_map[test_singer_name]).includes(song_name)){
                        videoId_list.push(videoId_map[test_singer_name][song_name])
                    }
                }
                console.log(videoId_list)
                return videoId_list
            },
            getTargetSong: function(){
                singer_name = plot_data[this.singer_id].name
                song_name = song_list[this.song_id]
                return [videoId_map[singer_name][song_name]]
            }

        }
    })

    function moveUp(){
        singer_name = plot_data[app.singer_id].name
        for(var i = app.song_id - 1; i >= 0; i--){
            test_song_name = song_list[i]
            if(Object.keys(videoId_map[singer_name]).includes(test_song_name)){
                app.song_id = i;
                break;
            }
        }
    }

    function moveDown(){
        singer_name = plot_data[app.singer_id].name
        for(var i = app.song_id + 1; i < song_list.length; i++){
            test_song_name = song_list[i]
            if(Object.keys(videoId_map[singer_name]).includes(test_song_name)){
                app.song_id = i;
                break;
            }
        }
    }

    function moveRight(){
        song_name = song_list[app.song_id]
        for(var i = app.singer_id + 1; i < plot_data.length; i++){
            test_singer_name = plot_data[i].name
            if(Object.keys(videoId_map[test_singer_name]).includes(song_name)){
                app.singer_id = i;
                break;
            }
        }
    }

    function moveLeft(){
        song_name = song_list[app.song_id]
        for(var i = app.singer_id - 1; i >= 0; i--){
            test_singer_name = plot_data[i].name
            if(Object.keys(videoId_map[test_singer_name]).includes(song_name)){
                app.singer_id = i;
                break;
            }
        }
    }

    document.onkeydown = evt =>{
        evt = evt || window.event;
        //up
        if (evt.keyCode == 38) {
            moveUp()
        }
        //down
        if (evt.keyCode == 40) {
            moveDown()
        }
        //right
        if (evt.keyCode == 39) {
            moveRight()
        }
        //left
        if (evt.keyCode == 37) {
            moveLeft()
        }
    }

    var touchStartX, touchStartY, touchMoveX, touchMoveY;
    document.addEventListener('touchstart', function(evt){
        event.preventDefault()
        touchStartX = evt.touches[0].pageX;
        touchStartY = evt.touches[0].pageY;
    }, {passive: false})

    document.addEventListener('touchmove', function(evt){
        event.preventDefault()
        touchMoveX = evt.changedTouches[0].pageX
        touchMoveY = evt.changedTouches[0].pageY
    }, {passive: false})

    document.ontouchend = evt => {
        xDiff = Math.abs(touchStartX - touchMoveX)
        yDiff = Math.abs(touchStartY - touchMoveY)
        if(xDiff > yDiff){
            if(touchStartX > touchMoveX + 25){
                moveRight()
            }else if(touchStartX - 25 < touchMoveX){
                moveLeft()
            }
        }else{
            if(touchStartY > touchMoveY + 25){
                moveDown()
            }else if(touchStartY - 25 < touchMoveY){
                moveUp()
            }
        }
    }

    window.onresize = evt => {
        app.width = window.innerWidth
        app.height = window.innerHeight
        console.log(app.width)
    }
}