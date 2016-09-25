Backbone.$ = $;

var router = Backbone.Router.extend({
  routes: {
    'search?q=:query': 'search'
  },

  search: function(query) {
    var search = new Search();

    search.save('query', query, {'success': function(searchResponse) {
      var div = document.createElement('div');
      div.innerText = searchResponse.get('query');
      document.body.appendChild(div);
    }});
  }
});

var Search = Backbone.Model.extend({
  urlRoot: '/api/v1/searches'
});


$('input[name=query]').keypress(function(e) {
  if(e.which === 13) {
    window.location.hash = "/search?q=" + encodeURIComponent(e.target.value);
  }
});

Backbone.history.start();

new router();
