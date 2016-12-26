// Initialize your app
var myApp = new Framework7({
  precompileTemplates: true,
  swipePanel: 'left',
});

// Export selectors engine
var $$ = Dom7;

var alltype = ''
      
// Loading flag
      
// Last loaded index
var lastIndex = $$('.list-block li').length;
      
// Max items to load
var maxItems = 60;
      
// Append items per load
var itemsPerLoad = 10;
      
jump = function () { 
  var mainView = myApp.addView('.view',{'dynamicNavbar':true});
  mainView.router.load($$('#myPage').html());
  return false
}

loading = false

update = function () {    
    if (loading == true){
	return 
    }
    lastIndex = $$('.list-block-icyjob li').length;
    loading = true
    $$.getJSON('/api/article', {offset:lastIndex,alltype:alltype}, function (data) {
        if(data.length == 0){
	  // 加载完毕，则注销无限加载事件，以防不必要的加载
	  myApp.detachInfiniteScroll($$('.infinite-scroll'));
	  // 删除加载提示符
	  $$('.infinite-scroll-preloader').hide();
	  myApp.alert('没有了‘(*>﹏<*)′ ~');
	  loading = false
	  return;
	}
        var html = '';
        for (var i = 0; i < data.length; i++) {
          
	  var templatecontext = $$('#jobItem').html();
	  console.log(templatecontext)
	  var compiledTemplate = Template7.compile(templatecontext);
	  item = data[i]
	  var context = {
	    title: item.title,
	    domain: item.domain,
	    time: item.time,
	  };
	  var htmlcompiled = templatecontext
	  htmlcompiled = htmlcompiled.replace('title_template',item.title)
	  htmlcompiled = htmlcompiled.replace('domain_template',item.domain)
	  htmlcompiled = htmlcompiled.replace('time_template',item.time)
	  htmlcompiled = htmlcompiled.replace('id_template',item.id)
	  //var htmlcompiled = compiledTemplate(context);
          html += htmlcompiled;
        }
        $$('.list-block-icyjob ul').append(html);
          // Update last loaded index
          lastIndex = $$('.list-block-icyjob li').length;
        $$('.swipeout-content').on('click', jump)
        loading = false
    });

    /*
    setTimeout(function () {
        // Generate new items HTML
        var html = '';
        for (var i = lastIndex + 1; i <= lastIndex + itemsPerLoad; i++) {
          html += $$('#jobItem').html();
        }
        // Append new items
        $$('.list-block ul').append(html);
          // Update last loaded index
          lastIndex = $$('.list-block li').length;
        $$('.swipeout-content').on('click', jump)
    }, 1000);
    */
}

$$('.swipeout-content').on('click', jump)

var ptrContent = $$('.pull-to-refresh-content');

ptrContent.on('refresh', function (e) {
	$$('.list-block-icyjob ul').html("");

	//var mainView = myApp.addView('.view-main');
	update()
	//mainView.router.refreshPage()
        setTimeout(function () {
		myApp.pullToRefreshDone();
		myApp.attachInfiniteScroll($$('.infinite-scroll'));
		$$('.infinite-scroll-preloader').show();
	},600);
});

// Attach 'infinite' event handler
$$('.infinite-scroll').on('infinite',update);



$$('.panel-left').on('close', function () {
	taglist = ''
	tags = $$('.typecheck')
	tags.each(function(){
		tag = $$(this)
		if(tag.prop("checked") == true){
    			taglist += ',' + tag.prop('value')
		}
	});
	jobtype = $$('#select-jobtype').prop('value')

	alltype = jobtype + taglist
	$$('.list-block-icyjob ul').html("");
	myApp.attachInfiniteScroll($$('.infinite-scroll'));
	$$('.infinite-scroll-preloader').show();

	update()
});

