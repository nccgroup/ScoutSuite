(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[83],{599:function(e,t,n){"use strict";n.r(t);var r=n(1),i=n(15),c=(n(0),n(16)),a=n.n(c),o=n(739),l=(n(91),n(744)),s=n(71);t.default=function(e){var t=e.data;if(!t)return null;var n=a()(t,["item","protocols"],{}),c=a()(t,["item","options"],{}),u=a()(t,["item","ciphers"],{}),b=a()(t,["item","PolicyAttributeDescriptions"],[]),d="SSLNegotiationPolicyType"===a()(t,["item","PolicyTypeName"]),j=function(e){return Object(r.jsx)("div",{children:e.map((function(e,t){var n=Object(i.a)(e,2),c=n[0],a=n[1];return Object(r.jsx)(s.a,{label:c,value:a},t)}))})};return Object(r.jsx)(o.a,{data:t,children:d?Object(r.jsxs)(l.b,{children:[Object(r.jsx)(l.a,{title:"Protocols",children:j(Object.entries(n))}),Object(r.jsx)(l.a,{title:"Options",children:j(Object.entries(c))}),Object(r.jsx)(l.a,{title:"Ciphers",children:j(Object.entries(u).filter((function(e){return"true"===Object(i.a)(e,2)[1]})))})]}):Object(r.jsx)(l.b,{children:Object(r.jsx)(l.a,{title:"Attributes",children:j(b.map((function(e){return[e.AttributeName,e.AttributeValue]})))})})})}},736:function(e,t,n){"use strict";n.d(t,"a",(function(){return a})),n.d(t,"b",(function(){return o})),n.d(t,"c",(function(){return l}));var r=n(0),i=n.n(r),c={path_to_issue:[],item:{}},a=i.a.createContext(c),o=i.a.createContext(""),l=i.a.createContext((function(){}))},737:function(e,t,n){"use strict";var r=n(1),i=n(0),c=n(736),a=n(91);t.a=function(e){var t=e.path,n=e.children,o=Object(i.useContext)(c.b);return Object(r.jsx)(c.b.Provider,{value:Object(a.a)(o,t),children:n})}},738:function(e,t,n){"use strict";var r=n(13),i=n(1),c=n(0),a=n(732),o=n(9),l=n.n(o),s=n(16),u=n.n(s),b=n(14),d=n.n(b),j=n(736),f=n(91),p=n(71),v=(n(740),n(723)),O=n(216),h=n.n(O),x=n(741),m=n.n(x),P=n(217),g=n(151),C=function(e){var t=e.service,n=e.finding,r=e.path,o=Object(c.useContext)(g.a),l=o.exceptions,s=o.addException,b=o.removeException,d=Object(P.b)().enqueueSnackbar,j=u()(l,[t,n],[]).includes(r);return Object(i.jsx)(a.a,{title:j?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(i.jsx)(v.a,{size:"small",className:"exception-btn",onClick:j?function(){b(t,n,r),d("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){s(t,n,r),d("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:j?Object(i.jsx)(m.a,{}):Object(i.jsx)(h.a,{})})})},A=n(34),y=function(e){var t,n=e.label,o=e.separator,s=e.valuePath,b=e.errorPath,v=e.className,O=e.inline,h=e.tooltip,x=e.tooltipProps,m=e.renderValue,P=e.basePathOverwrite,g=Object(A.g)(),y=Object(c.useContext)(j.a),N=Object(c.useContext)(j.b),S=Object(c.useContext)(j.c),k=Object(f.a)(P||N,s),E=m(e.value||u()(y.item,k,e.value));("boolean"===typeof E&&(E=String(E)),b)?t=(d()(b)?b:[b]).map((function(e){return Object(f.a)(P||N,e)})):t=[k];var _=t.some((function(e){return y.path_to_issues.includes(e)})),w=y.level;if(Object(c.useEffect)((function(){_&&S(w)}),[w]),void 0===E||null===E)return null;var z=Object(i.jsx)(C,{service:g.service,finding:g.finding,path:"".concat(y.path,".").concat(t[0])}),D=Object(i.jsxs)("span",{className:l()(_&&l()("issue",w)),children:[E,_&&z]});return Object(i.jsx)(p.a,{className:l()(v,"partial-value",{inline:O}),label:n,separator:o,value:h?Object(i.jsx)(a.a,Object(r.a)(Object(r.a)({title:E},x),{},{children:D})):D})};y.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=y},739:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return a.a})),n.d(t,"c",(function(){return o.a}));var r=n(1),i=(n(0),n(736)),c=(n(91),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(r.jsx)(i.a.Provider,{value:t,children:n})}),a=n(737),o=n(738)},740:function(e,t,n){},741:function(e,t,n){"use strict";var r=n(36),i=n(38);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var c=i(n(0)),a=(0,r(n(39)).default)(c.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=a},744:function(e,t,n){"use strict";n.d(t,"a",(function(){return b})),n.d(t,"b",(function(){return l.b}));var r=n(1),i=n(15),c=n(0),a=n(9),o=n.n(a),l=n(126),s=n(736),u=n(65),b=(n(745),function(e){var t=e.title,n=e.isSelected,a=e.disabled,b=e.onClick,d=e.children,j=Object(c.useState)(""),f=Object(i.a)(j,2),p=f[0],v=f[1],O=p?Object(r.jsxs)(r.Fragment,{children:[t,u.a[p].icon]}):t;return Object(r.jsx)(s.c.Provider,{value:v,children:Object(r.jsx)(l.a,{title:O,className:o()("partial-tab-pane",p),isSelected:n,disabled:a,onClick:b,children:d})})})},745:function(e,t,n){}}]);
//# sourceMappingURL=83.e7b4a0fc.chunk.js.map