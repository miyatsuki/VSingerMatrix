Vue.config.devtools = true;

onload = function() {
    const app = new Vue({
      el: '#app',
      data: {
        items: plot_data,
        query: "",
        selected_singer_id: -1
      }
    })
};
