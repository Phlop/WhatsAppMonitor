
function openModalDialog() {
    Ext.onReady(function() {
        Ext.create('Ext.window.Window', {
        title: 'Hello',
        height: Ext.getBody().getViewSize().height*0.8,
        width: Ext.getBody().getViewSize().width*0.8,
        minWidth:'730',
        minHeight:'450',
        layout: 'fit',
        itemId : 'popUpWin',        
        modal:true,
        shadow:false,
        resizable:true,
        constrainHeader:true,
        items: [{
            xtype: 'box',
            autoEl: {
                     tag: 'iframe',
                     src: '2.html',
                     frameBorder:'0'
            }
        }]
        }).show();
  });
}
function closeExtWin(isSubmit) {
     Ext.ComponentQuery.query('#popUpWin')[0].close();
     if (isSubmit) {
          document.forms[0].userAction.value = "refresh";
          document.forms[0].submit();
    }
}