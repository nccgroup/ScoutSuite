(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[62],{585:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(15)),c=n.n(r),i=n(640),l=n(103),s=n(104),o=n(642);t.default=function(e){var t,n=e.data,r=c()(n,["item"],{});return n?Object(a.jsxs)(i.a,{data:n,children:[Object(a.jsxs)(o.a,{children:[Object(a.jsx)(i.c,{label:"Project ID",valuePath:"project_id"}),Object(a.jsx)(i.c,{label:"Automatic Backups",valuePath:"automatic_backup_enabled",renderValue:l.c}),Object(a.jsx)(i.c,{label:"Last Backup",valuePath:"last_backup_timestamp",renderValue:l.h}),Object(a.jsx)(i.c,{label:"Logs",valuePath:"log_enabled",renderValue:l.c}),Object(a.jsx)(i.c,{label:"SSL Required",valuePath:"ssl_required",renderValue:l.c}),Object(a.jsx)(i.c,{label:"Public IP Address",valuePath:"public_ip",renderValue:l.n}),Object(a.jsx)(i.c,{label:"Private IP Address",valuePath:"private_ip",renderValue:l.n}),Object(a.jsx)(i.c,{label:"Authorized Networks",valuePath:"authorized_networks",renderValue:l.n})]}),Object(a.jsx)(s.b,{children:Object(a.jsx)(s.a,{title:"Authorized Networks",children:(t=r.authorized_networks,t&&0!==t.length?Object(a.jsx)("ul",{children:t.map((function(e,t){return Object(a.jsx)("li",{children:Object(a.jsx)(i.c,{errorPath:"authorized_networks.".concat(t,".open_to_the_world"),value:e})},t)}))}):Object(a.jsx)("span",{children:"None"}))})})]}):null}},637:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return l})),n.d(t,"c",(function(){return s}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),l=r.a.createContext(""),s=r.a.createContext((function(){}))},638:function(e,t,n){"use strict";var a=n(19),r=n(1),c=n(0),i=n(633),l=n(7),s=n.n(l),o=n(15),u=n.n(o),d=n(10),b=n.n(d),j=n(637),h=n(103),p=n(83),v=(n(641),n(624)),f=n(191),x=n.n(f),O=n(192),P=n(130),m=function(e){var t=e.service,n=e.finding,a=e.path,l=Object(c.useContext)(P.a),s=l.exceptions,o=l.addException,d=Object(O.b)().enqueueSnackbar,b=u()(s,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:"Add to exception list",placement:"top",arrow:!0,children:Object(r.jsx)(v.a,{disabled:b,size:"small",startIcon:Object(r.jsx)(x.a,{}),className:"exception-btn",onClick:function(){o(t,n,a),d("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:"Add"})})},_=n(29),k=function(e){var t,n=e.label,l=e.separator,o=e.valuePath,d=e.errorPath,v=e.className,f=e.inline,x=e.tooltip,O=e.tooltipProps,P=e.renderValue,k=e.basePathOverwrite,g=Object(_.g)(),w=Object(c.useContext)(j.a),A=Object(c.useContext)(j.b),C=Object(c.useContext)(j.c),N=Object(h.a)(k||A,o),V=P(e.value||u()(w.item,N,e.value));("boolean"===typeof V&&(V=String(V)),d)?t=(b()(d)?d:[d]).map((function(e){return Object(h.a)(k||A,e)})):t=[N];var z=t.some((function(e){return w.path_to_issues.includes(e)})),I=w.level;if(Object(c.useEffect)((function(){z&&C(I)}),[I]),void 0===V||null===V)return null;var D=Object(r.jsx)(m,{service:g.service,finding:g.finding,path:"".concat(w.path,".").concat(t[0])}),L=Object(r.jsxs)("span",{className:s()(z&&s()("issue",I)),children:[V,z&&D]});return Object(r.jsx)(p.a,{className:s()(v,"partial-value",{inline:f}),label:n,separator:l,value:x?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:V},O),{},{children:L})):L})};k.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=k},639:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(637),i=n(103);t.a=function(e){var t=e.path,n=e.children,l=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(l,t),children:n})}},640:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return l.a}));var a=n(1),r=(n(0),n(637)),c=(n(103),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(639),l=n(638)},641:function(e,t,n){},642:function(e,t,n){"use strict";var a=n(1);n(0),n(643);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},643:function(e,t,n){}}]);
//# sourceMappingURL=62.25503620.chunk.js.map