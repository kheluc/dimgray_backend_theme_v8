/*
# -*- encoding: utf-8 -*-
*/


openerp.dimgray_backend_theme_v8 = function(instance, local) {
	var _t = instance.web._t;
	openerp_FieldMany2ManyTagsMultiSelection(instance);
	openerp_listview_html_widget(instance);
	web_listview_sticky(instance);

	
	var QWeb = instance.web.qweb;
	instance.web.Client.include({

		show_annoucement_bar : function() {
			return;
		},

		bind_events : function() {
			var self = this;
			this._super();

			var root = self.$el.parents();
			$("#oe_main_menu_navbar.navbar").css("padding-left", "220px");
			var elem_sm = $("<button id='leftbar_toggle' type='button' class='navbar-toggle left'><span class='fa fa-th' style='color:#ffffff;font-size: 25px;'></span></button>");
			elem_sm.prependTo(root.find('.navbar-header'));
			 $(document).ready(function() {
 $('.page-loading').show();
});

			self.$el.on('click', '#leftbar_toggle', function() {
				var leftbar = root.find('.oe_leftbar');
				if (leftbar.css('display') == 'none') {
					leftbar.removeClass("hide");
					$("#oe_main_menu_navbar.navbar").css("padding-left", "220px");
					leftbar.addClass("show");
				} else {
					$("#oe_main_menu_navbar.navbar").css("padding-left", "0px");
					leftbar.removeClass("show");
					leftbar.addClass("hide");
				}
			});

			$('.oe_application').click(function () {
                var leftbar = root.find('.oe_leftbar');
				$("#oe_main_menu_navbar.navbar").css("padding-left", "0px");
                leftbar.removeClass("show");
                leftbar.addClass("hide");
            });

            $('ul.nav.navbar-nav.navbar-left.oe_application_menu_placeholder li a').click(function () {
                var leftbar = root.find('.oe_leftbar');
               if (leftbar.css('display') == 'none') {
					leftbar.removeClass("hide");
					$("#oe_main_menu_navbar.navbar").css("padding-left", "220px");
					leftbar.addClass("show");
				}
            });


		}
	});

	instance.web.Menu.include({
		reflow : function(behavior) {
			var self = this;
			var $more_container = this.$('#menu_more_container').hide();
			var $more = this.$('#menu_more');
			var $systray = this.$el.parents().find('.oe_systray');

			$more.children('li').insertBefore($more_container);
			// Pull all the items out of the more menu

			// 'all_outside' beahavior should display all the items, so hide the more menu and exit
			if (behavior === 'all_outside') {
				// Show list of menu items
				self.$el.show();
				this.$el.find('li').show();
				$more_container.hide();
				return;
			}

			// Hide all menu items
			var $toplevel_items = this.$el.find('li').not($more_container).not($systray.find('li')).hide();
			// Show list of menu items (which is empty for now since all menu items are hidden)
			self.$el.show();
			$toplevel_items.each(function() {
				var remaining_space = self.$el.parent().width() - $more_container.outerWidth() - 75;
				self.$el.parent().children(':visible').each(function() {
					remaining_space -= $(this).outerWidth();
				});

				if ($(this).width() >= remaining_space) {
					return false;
					// the current item will be appended in more_container
				}
				$(this).show();
				// show the current item in menu bar
			});
			$more.append($toplevel_items.filter(':hidden').show());
			$more_container.toggle(!!$more.children().length);
			// Hide toplevel item if there is only one
			var $toplevel = self.$el.children("li:visible");
			if ($toplevel.length === 1) {
				$toplevel.hide();
			}
		},

		open_menu : function(id) {
			var self = this;

			var root = self.$el.parents();
			var oe_main_menu_placeholder = root.find('#oe_main_menu_placeholder');

			if (oe_main_menu_placeholder.hasClass("in")) {
				oe_main_menu_placeholder.removeClass("in");
			}

			this._super(id);
		}
	});
};
