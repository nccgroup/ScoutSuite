(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[36],{553:function(e,t,n){"use strict";n.r(t);var a=n(18),r=n(1),c=(n(0),n(15)),i=n.n(c),l=(n(103),n(640)),s=n(645),o=n(642);t.default=function(e){var t=e.data;if(!t)return null;var n=i()(t,["item","parameters"]);return Object(r.jsxs)(l.a,{data:t,children:[Object(r.jsxs)(o.a,{children:[Object(r.jsx)(l.c,{label:"ARN",valuePath:"arn"}),Object(r.jsx)(l.c,{label:"Descripition",valuePath:"description"}),Object(r.jsx)(l.c,{label:"Group Family",valuePath:"family"}),Object(r.jsx)(l.c,{label:"Default Parameter Group",valuePath:"is_default"})]}),Object(r.jsx)(s.b,{children:Object(r.jsx)(s.a,{title:"Parameters",children:Object(r.jsx)("div",{children:Object.entries(n).map((function(e,t){var n=Object(a.a)(e,2),c=n[0],i=n[1];return Object(r.jsx)(l.c,{label:c,value:i.value,errorPath:c},t)}))})})})]})}},637:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return l})),n.d(t,"c",(function(){return s}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),l=r.a.createContext(""),s=r.a.createContext((function(){}))},638:function(e,t,n){"use strict";var a=n(19),r=n(1),c=n(0),i=n(633),l=n(7),s=n.n(l),o=n(15),u=n.n(o),b=n(10),d=n.n(b),j=n(637),f=n(103),v=n(83),p=(n(641),n(624)),h=n(191),O=n.n(h),x=n(192),m=n(130),P=function(e){var t=e.service,n=e.finding,a=e.path,l=Object(c.useContext)(m.a),s=l.exceptions,o=l.addException,b=Object(x.b)().enqueueSnackbar,d=u()(s,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:"Add to exception list",placement:"top",arrow:!0,children:Object(r.jsx)(p.a,{disabled:d,size:"small",startIcon:Object(r.jsx)(O.a,{}),className:"exception-btn",onClick:function(){o(t,n,a),b("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:"Add"})})},C=n(29),g=function(e){var t,n=e.label,l=e.separator,o=e.valuePath,b=e.errorPath,p=e.className,h=e.inline,O=e.tooltip,x=e.tooltipProps,m=e.renderValue,g=e.basePathOverwrite,N=Object(C.g)(),A=Object(c.useContext)(j.a),k=Object(c.useContext)(j.b),w=Object(c.useContext)(j.c),D=Object(f.a)(g||k,o),S=m(e.value||u()(A.item,D,e.value));("boolean"===typeof S&&(S=String(S)),b)?t=(d()(b)?b:[b]).map((function(e){return Object(f.a)(g||k,e)})):t=[D];var _=t.some((function(e){return A.path_to_issues.includes(e)})),y=A.level;if(Object(c.useEffect)((function(){_&&w(y)}),[y]),void 0===S||null===S)return null;var E=Object(r.jsx)(P,{service:N.service,finding:N.finding,path:"".concat(A.path,".").concat(t[0])}),I=Object(r.jsxs)("span",{className:s()(_&&s()("issue",y)),children:[S,_&&E]});return Object(r.jsx)(v.a,{className:s()(p,"partial-value",{inline:h}),label:n,separator:l,value:O?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:S},x),{},{children:I})):I})};g.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=g},639:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(637),i=n(103);t.a=function(e){var t=e.path,n=e.children,l=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(l,t),children:n})}},640:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return l.a}));var a=n(1),r=(n(0),n(637)),c=(n(103),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(639),l=n(638)},641:function(e,t,n){},642:function(e,t,n){"use strict";var a=n(1);n(0),n(643);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},643:function(e,t,n){},644:function(e,t,n){},645:function(e,t,n){"use strict";n.d(t,"a",(function(){return b})),n.d(t,"b",(function(){return s.b}));var a=n(1),r=n(18),c=n(0),i=n(7),l=n.n(i),s=n(104),o=n(637),u=n(56),b=(n(644),function(e){var t=e.title,n=e.isSelected,i=e.disabled,b=e.onClick,d=e.children,j=Object(c.useState)(""),f=Object(r.a)(j,2),v=f[0],p=f[1],h=v?Object(a.jsxs)(a.Fragment,{children:[t,u.a[v].icon]}):t;return Object(a.jsx)(o.c.Provider,{value:p,children:Object(a.jsx)(s.a,{title:h,className:l()("partial-tab-pane",v),isSelected:n,disabled:i,onClick:b,children:d})})})}}]);
//# sourceMappingURL=36.8f789880.chunk.js.map