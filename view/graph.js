Vue.config.devtools = true;

onload = function() {
    const app = new Vue({
      el: '#app',
      data: {
        items: plot_data,
        videoId_map: videoId_map,
        query: "",
        selected_singer_id: -1
      }
    })
};
