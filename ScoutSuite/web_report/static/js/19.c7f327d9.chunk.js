(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[19],{632:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(742)),c=n(739),i=n(91),l=n(744),s=n(72),u=n(750),o=function(e){return Object(i.l)(e,"",(function(e){return function(e){return Object(a.jsx)(s.a,{service:"aad",resource:"groups",id:e.id,name:e.name})}(e)}))};t.default=function(e){var t=e.data,n=e.item,s=Object(u.a)("aad","groups",n.groups).data;return t?Object(a.jsxs)(c.a,{data:t,children:[Object(a.jsxs)(r.a,{children:[Object(a.jsx)(c.c,{label:"Principal Name",valuePath:"name",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Display Name",valuePath:"display_name",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Given Name",valuePath:"given_name",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Surname",valuePath:"surname",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Mail Nickname",valuePath:"mail_nickname",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Mail",valuePath:"mail",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Sign-In Names",valuePath:"sign_in_names",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Type",valuePath:"user_type",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Status",valuePath:"account_enabled",renderValue:i.c}),Object(a.jsx)(c.c,{label:"Usage Location",valuePath:"usage_location",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Deletion Timestamp",valuePath:"deletion_timestamp",renderValue:i.q})]}),Object(a.jsx)(l.b,{children:Object(a.jsx)(l.a,{title:"Groups",children:o(s)})})]}):null}},736:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return l})),n.d(t,"c",(function(){return s}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),l=r.a.createContext(""),s=r.a.createContext((function(){}))},737:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(736),i=n(91);t.a=function(e){var t=e.path,n=e.children,l=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(l,t),children:n})}},738:function(e,t,n){"use strict";var a=n(13),r=n(1),c=n(0),i=n(732),l=n(9),s=n.n(l),u=n(16),o=n.n(u),b=n(14),d=n.n(b),j=n(736),f=n(91),v=n(71),p=(n(740),n(723)),O=n(216),h=n.n(O),x=n(741),m=n.n(x),P=n(217),g=n(151),_=function(e){var t=e.service,n=e.finding,a=e.path,l=Object(c.useContext)(g.a),s=l.exceptions,u=l.addException,b=l.removeException,d=Object(P.b)().enqueueSnackbar,j=o()(s,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:j?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(p.a,{size:"small",className:"exception-btn",onClick:j?function(){b(t,n,a),d("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){u(t,n,a),d("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:j?Object(r.jsx)(m.a,{}):Object(r.jsx)(h.a,{})})})},V=n(34),N=function(e){var t,n=e.label,l=e.separator,u=e.valuePath,b=e.errorPath,p=e.className,O=e.inline,h=e.tooltip,x=e.tooltipProps,m=e.renderValue,P=e.basePathOverwrite,g=Object(V.g)(),N=Object(c.useContext)(j.a),k=Object(c.useContext)(j.b),q=Object(c.useContext)(j.c),C=Object(f.a)(P||k,u),S=m(e.value||o()(N.item,C,e.value));("boolean"===typeof S&&(S=String(S)),b)?t=(d()(b)?b:[b]).map((function(e){return Object(f.a)(P||k,e)})):t=[C];var y=t.some((function(e){return N.path_to_issues.includes(e)})),w=N.level;if(Object(c.useEffect)((function(){y&&q(w)}),[w]),void 0===S||null===S)return null;var E=Object(r.jsx)(_,{service:g.service,finding:g.finding,path:"".concat(N.path,".").concat(t[0])}),A=Object(r.jsxs)("span",{className:s()(y&&s()("issue",w)),children:[S,y&&E]});return Object(r.jsx)(v.a,{className:s()(p,"partial-value",{inline:O}),label:n,separator:l,value:h?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:S},x),{},{children:A})):A})};N.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=N},739:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return l.a}));var a=n(1),r=(n(0),n(736)),c=(n(91),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(737),l=n(738)},740:function(e,t,n){},741:function(e,t,n){"use strict";var a=n(36),r=n(38);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var c=r(n(0)),i=(0,a(n(39)).default)(c.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=i},742:function(e,t,n){"use strict";var a=n(1);n(0),n(743);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},743:function(e,t,n){},744:function(e,t,n){"use strict";n.d(t,"a",(function(){return b})),n.d(t,"b",(function(){return s.b}));var a=n(1),r=n(15),c=n(0),i=n(9),l=n.n(i),s=n(126),u=n(736),o=n(65),b=(n(745),function(e){var t=e.title,n=e.isSelected,i=e.disabled,b=e.onClick,d=e.children,j=Object(c.useState)(""),f=Object(r.a)(j,2),v=f[0],p=f[1],O=v?Object(a.jsxs)(a.Fragment,{children:[t,o.a[v].icon]}):t;return Object(a.jsx)(u.c.Provider,{value:p,children:Object(a.jsx)(s.a,{title:O,className:l()("partial-tab-pane",v),isSelected:n,disabled:i,onClick:b,children:d})})})},745:function(e,t,n){},750:function(e,t,n){"use strict";n.d(t,"a",(function(){return u}));var a=n(37),r=n.n(a),c=n(73),i=n(15),l=n(0),s=n(152),u=function(e,t,n){var a=Object(l.useState)([]),u=Object(i.a)(a,2),o=u[0],b=u[1],d=Object(l.useState)(!0),j=Object(i.a)(d,2),f=j[0],v=j[1];return Object(l.useEffect)((function(){(function(){var a=Object(c.a)(r.a.mark((function a(){var c,i;return r.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:if(!(e&&t&&n)){a.next=15;break}return v(!0),a.prev=2,c=n.map((function(n){return s.b("services/".concat(e,"/resources/").concat(t,"/").concat(n))})),a.next=6,Promise.all(c);case 6:i=a.sent,console.info("useResources response",e,t,n,i),b(i),a.next=14;break;case 11:a.prev=11,a.t0=a.catch(2),console.error(a.t0.message);case 14:v(!1);case 15:case"end":return a.stop()}}),a,null,[[2,11]])})));return function(){return a.apply(this,arguments)}})()()}),[n]),{data:o,loading:f}}}}]);
//# sourceMappingURL=19.c7f327d9.chunk.js.map