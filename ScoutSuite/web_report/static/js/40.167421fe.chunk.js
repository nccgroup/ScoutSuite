(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[40],{570:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(642)),c=n(640),i=n(103),o=n(645);t.default=function(e){var t=e.data;return t?Object(a.jsxs)(c.a,{data:t,children:[Object(a.jsxs)(r.a,{children:[Object(a.jsx)(c.c,{label:"Name",valuePath:"name",renderValue:i.n}),Object(a.jsx)(c.c,{label:"Location",valuePath:"location",renderValue:i.n}),Object(a.jsx)(c.c,{label:"Provisioning State",valuePath:"provisioning_state",renderValue:i.n}),Object(a.jsx)(c.c,{label:"Tags",valuePath:"tags",renderValue:function(e){return Object(i.k)(e,i.n)}}),Object(a.jsx)(c.c,{label:"Resource group",valuePath:"resource_group_name",renderValue:i.n})]}),Object(a.jsx)(o.b,{children:Object(a.jsx)(o.a,{title:"Attached Network Interfaces"})})]}):null}},637:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return o})),n.d(t,"c",(function(){return l}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),o=r.a.createContext(""),l=r.a.createContext((function(){}))},638:function(e,t,n){"use strict";var a=n(19),r=n(1),c=n(0),i=n(633),o=n(7),l=n.n(o),s=n(15),u=n.n(s),d=n(10),b=n.n(d),j=n(637),f=n(103),v=n(83),h=(n(641),n(624)),p=n(191),O=n.n(p),x=n(192),m=n(130),P=function(e){var t=e.service,n=e.finding,a=e.path,o=Object(c.useContext)(m.a),l=o.exceptions,s=o.addException,d=Object(x.b)().enqueueSnackbar,b=u()(l,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:"Add to exception list",placement:"top",arrow:!0,children:Object(r.jsx)(h.a,{disabled:b,size:"small",startIcon:Object(r.jsx)(O.a,{}),className:"exception-btn",onClick:function(){s(t,n,a),d("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:"Add"})})},g=n(29),C=function(e){var t,n=e.label,o=e.separator,s=e.valuePath,d=e.errorPath,h=e.className,p=e.inline,O=e.tooltip,x=e.tooltipProps,m=e.renderValue,C=e.basePathOverwrite,N=Object(g.g)(),k=Object(c.useContext)(j.a),A=Object(c.useContext)(j.b),V=Object(c.useContext)(j.c),_=Object(f.a)(C||A,s),w=m(e.value||u()(k.item,_,e.value));("boolean"===typeof w&&(w=String(w)),d)?t=(b()(d)?d:[d]).map((function(e){return Object(f.a)(C||A,e)})):t=[_];var S=t.some((function(e){return k.path_to_issues.includes(e)})),I=k.level;if(Object(c.useEffect)((function(){S&&V(I)}),[I]),void 0===w||null===w)return null;var D=Object(r.jsx)(P,{service:N.service,finding:N.finding,path:"".concat(k.path,".").concat(t[0])}),E=Object(r.jsxs)("span",{className:l()(S&&l()("issue",I)),children:[w,S&&D]});return Object(r.jsx)(v.a,{className:l()(h,"partial-value",{inline:p}),label:n,separator:o,value:O?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:w},x),{},{children:E})):E})};C.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=C},639:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(637),i=n(103);t.a=function(e){var t=e.path,n=e.children,o=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(o,t),children:n})}},640:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return o.a}));var a=n(1),r=(n(0),n(637)),c=(n(103),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(639),o=n(638)},641:function(e,t,n){},642:function(e,t,n){"use strict";var a=n(1);n(0),n(643);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},643:function(e,t,n){},644:function(e,t,n){},645:function(e,t,n){"use strict";n.d(t,"a",(function(){return d})),n.d(t,"b",(function(){return l.b}));var a=n(1),r=n(18),c=n(0),i=n(7),o=n.n(i),l=n(104),s=n(637),u=n(56),d=(n(644),function(e){var t=e.title,n=e.isSelected,i=e.disabled,d=e.onClick,b=e.children,j=Object(c.useState)(""),f=Object(r.a)(j,2),v=f[0],h=f[1],p=v?Object(a.jsxs)(a.Fragment,{children:[t,u.a[v].icon]}):t;return Object(a.jsx)(s.c.Provider,{value:h,children:Object(a.jsx)(l.a,{title:p,className:o()("partial-tab-pane",v),isSelected:n,disabled:i,onClick:d,children:b})})})}}]);
//# sourceMappingURL=40.167421fe.chunk.js.map