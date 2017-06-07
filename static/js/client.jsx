var $            = require('jquery'),
    React        = require('react'),
    ReactDOM     = require('react-dom'),
    DjangoCSRF   = require('./django-csrf'),
    SefariaReact = require('./s2');

$(function() {
  var container = document.getElementById('s2');
  var component;

  if (DJANGO_VARS.inReaderApp) {
    DjangoCSRF.init();
    SefariaReact.unpackDataFromProps(DJANGO_VARS.propsJSON);
    component = React.createElement(SefariaReact.ReaderApp, DJANGO_VARS.propsJSON);
    ReactDOM.render(component, container);
  } else {
    var settings = {
      language: DJANGO_VARS.contentLang,
      layoutDefault: $.cookie("layoutDefault") || "segmented",
      layoutTalmud:  $.cookie("layoutTalmud")  || "continuous",
      layoutTanakh:  $.cookie("layoutTanakh")  || "segmented",
      color:         $.cookie("color")         || "light",
      fontSize:      $.cookie("fontSize")      || 62.5
    };
    var multiPanel    = $(window).width() > 600;
    component = React.createElement(SefariaReact.ReaderApp, {
      headerMode: true,
      multiPanel: multiPanel,
      initialRefs: [],
      initialFilter: [],
      initialMenu: null,
      initialQuery: null,
      initialSheetsTag: null,
      initialNavigationCategories: [],
      initialSettings: settings,
      initialPanels: [],
      interfaceLang: DJANGO_VARS.interfaceLang
    });
    ReactDOM.render(component, container);
    ReactDOM.render(React.createElement(SefariaReact.Footer), document.getElementById('footer'));

  }
});