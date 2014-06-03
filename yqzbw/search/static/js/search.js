$(function () {
	$('.category,.type,.only').click(function () {
	  if ($(this).hasClass('disabled')==false&&$(this).hasClass('active')==false&&$(this).hasClass('badge-important')==false) {
  	  var value=$('#kw').val();
  	      nu = $(this).attr('id');
  	  if (value) {
  	    if (nu!='btn'&&nu!='times') {
    	    if (nu<5) {
    	      $('.category').removeClass('active');
    	      $('#'+nu+'').addClass('active');
    	      $('.type').removeClass('badge-important').addClass('badge-success');
    	      $('#'+(nu-(-5))).removeClass('badge-success').addClass('badge-important');
          }else if (nu<10) {
            $('.category').removeClass('active');
    	      $('#'+(nu-5)).addClass('active');
    	      $('.type').removeClass('badge-important').addClass('badge-success');
    	      $('#'+nu).removeClass('badge-success').addClass('badge-important');
    	      var nu = nu-5;
          }else if (nu<23) {
            $('.only').removeClass('badge-important').addClass('badge-success');
          	if (nu==21) {
          	  $('#21').removeClass('badge-success').addClass('badge-important');
            	value='title:'+value.split(':').slice(-1)[0];
            }else if (nu==22) {
              $('#22').removeClass('badge-success').addClass('badge-important');
              value='content:'+value.split(':').slice(-1)[0];
            }else {
            	$('#20').removeClass('badge-success').addClass('badge-important');
            	value=value.split(':').slice(-1)[0];
            }
          }
        }else if (nu=='times') {
        	
        }
        var num = $('.category.active').attr('id');
            vvv = handle(value,num);
            val = handles(value,num);
        $('#chart').fadeOut();
        $('#pagination').fadeOut();
        $('#btn').addClass('disabled');
  	    $.getJSON("/hudie/?value="+vvv+"&sk=0&con="+val.con,function (data) {
  	      window.cou=parseInt(data.count/10)+1;
  	      $('#kw').val(value);
    	    $('#lc').fadeIn();
    	    if (data.result.length>0) {
          	$('#pagination').fadeIn();
          	$('#btn').removeClass('disabled');
      	    console.log(data);
      	    tables(data);
      	    if (cou==1) {
            	tables(data);
            	$('#pagination').fadeOut();
            }else {
      	      shuaye1(cou);
      	      $('#pagination').fadeIn();
      	    } 
          }else {
            $('#chart').fadeIn();
            $('#pagination').fadeOut();
            $('#btn').removeClass('disabled');
          	$('#chart').html('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;找到约 0 条结果<br />')
          }  	    
        });
      }else if (nu!='btn') {
        $('#pagination').fadeOut();
        $('#lc').fadeOut();
  	    $('.category').removeClass('active');
  	    $('#'+nu+'').addClass('active');
      }
    }	
  });
  $('#page').on('click','.page',function () {
    if ($(this).hasClass('disabled')==false&&$(this).hasClass('active')==false) {
  	  var nu = $('.page.active a').text();
  	  	  nt = $('.page.active').attr('id');
  	      di = $(this).attr('id');
  	  if ($(this).next().attr('id')=='down'&&$(this).text()!=1&&$(this).text()!=cou||$(this).prev().attr('id')=='up'&&$(this).text()!=1&&$(this).text()<parseInt(cou)) {
        num = parseInt($(this).text())+4;
      	shuaye(num);
      }else {
      	fanye(nu,di,nt);
      }
    }	  
  });
});
  function fanye(nu,di,nt) {
	  if (di=='down'&&$('.page.active').hasClass('end')==true&&nu!=cou-1) {
	    nu = parseInt(nu)+5;
	    shuaye(nu,15);
    }else if (di=='up'&&$('.page.active').hasClass('start')==true&&nu!=2) {
	    var nu = parseInt(nu)+3;
	    shuaye(nu,15);
    }else if (di=='down') {
    	$('.page').removeClass('active');
    	$('#'+nt).next().addClass('active');
    	$('#up').removeClass('disabled');
    	if (nu==cou-1) {
      	$('#down').addClass('disabled');
      }
    }else if (di=='up') {
    	$('.page').removeClass('active');
    	$('#'+nt).prev().addClass('active');
    	$('#down').removeClass('disabled');
    	if (nu==2) {
      	$('#up').addClass('disabled');
      }
    }else {
	    $('.page').removeClass('active');
	    $('#'+di+'').addClass('active');
	    if ($('.page.active').text()==1) {
      	$('#up').addClass('disabled');
      	$('#down').removeClass('disabled');
      }else if ($('.page.active').text()==cou) {
        $('#down').addClass('disabled');
        $('#up').removeClass('disabled');
      }else {
      	$('#up').removeClass('disabled');
      	$('#down').removeClass('disabled');
      }
    }
    var value=$('#kw').val();
        num = $('.category.active').attr('id');
        val = handle(value,num);
        sk  = $('.page.active').text()-1;
        $('#chart').fadeOut();
        $('#pagination').fadeOut();
        $.getJSON("/hudie/?value="+val+"&con="+values.con+"&sk="+sk,function (data) {
          tables(data);        
        });
  }
  function shuaye(nu,nt) {
    $('.page').removeClass('active');
    if (nu>cou) {
    	var bom = parseInt((cou-5)/4)*4+1;
    	    rmd = parseInt((cou-1)%4+5);
    	    pa = '<li class="page" id="up"><a><<</a></li>';
    	for (var i=0;i<rmd;i++) {
      	pa+= '<li class="page" id="'+(11+i)+'"><a>'+(bom+i)+'</a></li>';
      }
      pa+='<li class="page " id="down"><a>>></a></li>';
      $('#page').html(pa);
      $('#12').addClass('start');
      $('#15').addClass('active');
    }else {
	    pa = '<li class="page" id="up"><a><<</a></li>\
            <li class="page" id="11"><a>'+(parseInt(nu)-8)+'</a></li>\
            <li class="page start" id="12"><a>'+(parseInt(nu)-7)+'</a></li>\
            <li class="page" id="13"><a>'+(parseInt(nu)-6)+'</a></li>\
            <li class="page" id="14"><a>'+(parseInt(nu)-5)+'</a></li>\
            <li class="page" id="15"><a>'+(parseInt(nu)-4)+'</a></li>\
            <li class="page" id="16"><a>'+(parseInt(nu)-3)+'</a></li>\
            <li class="page" id="17"><a>'+(parseInt(nu)-2)+'</a></li>\
            <li class="page end" id="18"><a>'+(parseInt(nu)-1)+'</a></li>\
            <li class="page" id="19"><a>'+nu+'</a></li>\
            <li class="page" id="down"><a>>></a></li>';
      $('#page').html(pa);
      $('#15').addClass('active');
     
    }
    var value=$('#kw').val();
        num = $('.category.active').attr('id');
        val = handle(value,num);
        sk  = $('.page.active').text()-1;
        $('#chart').fadeOut();
        $('#pagination').fadeOut();
        $.getJSON("/hudie/?value="+values.res+"&con="+values.con+"&sk="+sk,function (data) {
          tables(data);        
        });
  }
  function shuaye1(nu) {
    if (nu<=9) {
	    pa = '<li class="page" id="up"><a><<</a></li>';
  	  for (var i=0;i<nu;i++) {
    	  pa+='<li class="page" id="'+(11+i)+'"><a>'+(i+1)+'</a></li>';
      }
    pa+='<li class="page" id="down"><a>>></a></li>';
    $('#page').html(pa);
    $('#11').addClass('active');
    $('#12').addClass('start');
    $('#up').addClass('disabled');
    }else {
      var nu = 9;
    	pa = '<li class="page" id="up"><a><<</a></li>\
            <li class="page" id="11"><a>'+(parseInt(nu)-8)+'</a></li>\
            <li class="page start" id="12"><a>'+(parseInt(nu)-7)+'</a></li>\
            <li class="page" id="13"><a>'+(parseInt(nu)-6)+'</a></li>\
            <li class="page" id="14"><a>'+(parseInt(nu)-5)+'</a></li>\
            <li class="page" id="15"><a>'+(parseInt(nu)-4)+'</a></li>\
            <li class="page" id="16"><a>'+(parseInt(nu)-3)+'</a></li>\
            <li class="page" id="17"><a>'+(parseInt(nu)-2)+'</a></li>\
            <li class="page end" id="18"><a>'+(parseInt(nu)-1)+'</a></li>\
            <li class="page" id="19"><a>'+nu+'</a></li>\
            <li class="page" id="down"><a>>></a></li>';
      $('#page').html(pa);
      $('#up').addClass('disabled');
      $('#11').addClass('active');
    }
  }
  function tables(res) {
    console.log(res)
	  var sel=res.con; 
	      num=res.count;
	      time=parseInt(res.usetime)/1000; 
	      res=res.result;
	      tb = '<p style="color:#999999;font-size:1em;margin-left:4%;">找到 '+num.format()+' 条结果,用时 '+time+' 秒</p>';
	  for (var i in res) {
      if (values.val.siteName) {
      	site=res[i]['siteName'].replace(values.val.siteName.$regex,'<b style="color:red;">'+values.val.siteName.$regex+'</b>');
      }else {
      	site=res[i]['siteName'];
      }
      if (values.val.title) {
      	tit=res[i]['title'].replace(values.val.title.$regex,'<b style="color:red;">'+values.val.title.$regex+'</b>');
      }else {
      	tit=res[i]['title'];
      }
      if (values.val.url) {
      	url=res[i]['url'].replace(values.val.url.$regex,'<b style="color:red;">'+values.val.url.$regex+'</b>');
      }else {
      	url=res[i]['url'];
      }  
	    tb+='<br /><ul style="list-style-type:none;">\
	             <li style="font-size:1.2em;" id="lil">\
	             <a style="color:#1E0FBE; text-decoration:none;" title="'+res[i]['title']+'" href="'+res[i]['url']+'" target="_blank">'+tit+'</a></li>\
	             <li id="lil" style="color:#006621;">'+url+'</li>\
	             <li>来自:'+res[i]['source']+'--'+site+'</li>\
               <li>发表时间:'+res[i]['ctime']+'<li>\
	             <li style="float:right;">入库时间:'+res[i]['gtime']+'&nbsp;--<i class="icon-camera">\
	             <a href="/tail/'+res[i]['id']+'" target="_blank"></i>数据快照</a></li></ul>';
	  $('#chart').fadeIn();
	  $('#pagination').fadeIn(); 
	  $('#chart').html(tb);
    }
  }
  function handles(dat,num) {
    var dt = dat.toLocaleLowerCase()
        c = {};
        console.log(dt);
    if (dt.indexOf('sitename:')>=0||dt.indexOf('title:')>=0||dt.indexOf('http:')>=0||dt.indexOf('content:')>=0) {
  	  var dt = dt.split(' ');
      for (var i in dt) {
        var s=dt[i].split(':');
        if (s[0]=='sitename'){
          c['siteName']={'$regex':s[1]};
        }else if (s[0]=='http') {
          c['url']={'$regex':dt[i].replace(/:/,'')};
        }else {
          c[s[0]]={'$regex':s[1]}
        }
      }
    }else {
    	c={'content':{'$regex':dt},'title':{'$regex':dt}};
    }
    if (c['siteName']&&c['title']) {
    	con = 'all';
    }else if (c['siteName']) {
    	con = 'siteName';
    }else if (c['title']) {
    	con = 'title';
    }else {
    	con = 0;
    }
    window.values={'val':c,'con':con};
    return values;
  }
  function handle(dat,num) {
    var dat = dat.replace(/:/g,'\:')
  	if (num!=0&&num!=4) {
      	var dat=dat+' AND info_flag:0'+num;
      }else if (num==4) {
      	var dat=dat+' AND info_flag:0401 info_flag:0401';
      }
    return dat;
  }
  Number.prototype.format = function() {
  return this.toFixed(1).replace(/(\d)(?=(\d{3})+\.)/g, "$1,").replace(/\../,'');
  };
  function getLocalTime(nS) {
        var now = new Date(parseInt(nS)*1000)
        return now.getFullYear()+'-'+(parseInt(now.getMonth())+1)+'-'+now.getDate()+' '+now.getHours()+':'+now.getMinutes()+':'+now.getSeconds();
        }
