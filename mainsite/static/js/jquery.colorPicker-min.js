!function($){var e,o,c=0,r={control:$('<div class="colorPicker-picker">&nbsp;</div>'),palette:$('<div id="colorPicker_palette" class="colorPicker-palette" />'),swatch:$('<div class="colorPicker-swatch">&nbsp;</div>'),hexLabel:$('<label for="colorPicker_hex">Hex</label>'),hexField:$('<input type="text" id="colorPicker_hex" />')},t="transparent",n;$.fn.colorPicker=function(e){return this.each(function(){var o=$(this),n=$.extend({},$.fn.colorPicker.defaults,e),i=$.fn.colorPicker.toHex(o.val().length>0?o.val():n.pickerDefault),l=r.control.clone(),a=r.palette.clone().attr("id","colorPicker_palette-"+c),s=r.hexLabel.clone(),d=r.hexField.clone(),f=a[0].id,h,u;if($.each(n.colors,function(e){h=r.swatch.clone(),n.colors[e]===t?(h.addClass(t).text("X"),$.fn.colorPicker.bindPalette(d,h,t)):(h.css("background-color","#"+this),$.fn.colorPicker.bindPalette(d,h)),h.appendTo(a)}),s.attr("for","colorPicker_hex-"+c),d.attr({id:"colorPicker_hex-"+c,value:i}),d.bind("keydown",function(e){if(13===e.keyCode){var c=$.fn.colorPicker.toHex($(this).val());$.fn.colorPicker.changeColor(c?c:o.val())}27===e.keyCode&&$.fn.colorPicker.hidePalette()}),d.bind("keyup",function(e){var c=$.fn.colorPicker.toHex($(e.target).val());$.fn.colorPicker.previewColor(c?c:o.val())}),$('<div class="colorPicker_hexWrap" />').append(s).appendTo(a),a.find(".colorPicker_hexWrap").append(d),n.showHexField===!1&&(d.hide(),s.hide()),$("body").append(a),a.hide(),l.css("background-color",i),l.bind("click",function(){o.is(":not(:disabled)")&&$.fn.colorPicker.togglePalette($("#"+f),$(this))}),e&&e.onColorChange?l.data("onColorChange",e.onColorChange):l.data("onColorChange",function(){}),(u=o.data("text"))&&l.html(u),o.after(l),o.bind("change",function(){o.next(".colorPicker-picker").css("background-color",$.fn.colorPicker.toHex($(this).val()))}),o.val(i),"input"===o[0].tagName.toLowerCase())try{o.attr("type","hidden")}catch(k){o.css("visibility","hidden").css("position","absolute")}else o.hide();c++})},$.extend(!0,$.fn.colorPicker,{toHex:function(e){if(e.match(/[0-9A-F]{6}|[0-9A-F]{3}$/i))return"#"===e.charAt(0)?e:"#"+e;if(!e.match(/^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/))return!1;var o=[parseInt(RegExp.$1,10),parseInt(RegExp.$2,10),parseInt(RegExp.$3,10)],c=function(e){if(e.length<2)for(var o=0,c=2-e.length;c>o;o++)e="0"+e;return e};if(3===o.length){var r=c(o[0].toString(16)),t=c(o[1].toString(16)),n=c(o[2].toString(16));return"#"+r+t+n}},checkMouse:function(c,r){var t=o,n=$(c.target).parents("#"+t.attr("id")).length;c.target===$(t)[0]||c.target===e[0]||n>0||$.fn.colorPicker.hidePalette()},hidePalette:function(){$(document).unbind("mousedown",$.fn.colorPicker.checkMouse),$(".colorPicker-palette").hide()},showPalette:function(o){var c=e.prev("input").val();o.css({top:e.offset().top+e.outerHeight(),left:e.offset().left}),$("#color_value").val(c),o.show(),$(document).bind("mousedown",$.fn.colorPicker.checkMouse)},togglePalette:function(c,r){r&&(e=r),o=c,o.is(":visible")?$.fn.colorPicker.hidePalette():$.fn.colorPicker.showPalette(c)},changeColor:function(o){e.css("background-color",o),e.prev("input").val(o).change(),$.fn.colorPicker.hidePalette(),e.data("onColorChange").call(e,$(e).prev("input").attr("id"),o)},previewColor:function(o){e.css("background-color",o)},bindPalette:function(o,c,r){r=r?r:$.fn.colorPicker.toHex(c.css("background-color")),c.bind({click:function(e){n=r,$.fn.colorPicker.changeColor(r)},mouseover:function(e){n=o.val(),$(this).css("border-color","#598FEF"),o.val(r),$.fn.colorPicker.previewColor(r)},mouseout:function(c){$(this).css("border-color","#000"),o.val(e.css("background-color")),o.val(n),$.fn.colorPicker.previewColor(n)}})}}),$.fn.colorPicker.defaults={pickerDefault:"2a2a2a",colors:["2a2a2a","3d4044","57575a","808080","b4b4b9","e4e1d8","f2efea","FFFFFF","181c41","0f1c97","193b44","26416c","365d98","3B5998","007BB5","808bcf","a3bce4","00ACED","d92226","bf1d21","fffb22","ffca4c","FF00FF","FFCC00","FFFF00","00FF00","00FFFF","00CCFF","993366","C0C0C0","FF99CC","FFCC99","FFFF99","CCFFFF","99CCFF","FFFFFF"],addColors:[],showHexField:!0}}(jQuery);