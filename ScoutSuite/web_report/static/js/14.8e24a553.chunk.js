(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[14,80],{516:function(e,t,n){"use strict";n.r(t);var c=n(18),r=n(1),a=(n(0),n(640));n(661);t.default=function(e){var t=e.rules,n=e.type;return Object(r.jsxs)("table",{className:"rules-table",children:[Object(r.jsx)("thead",{children:Object(r.jsxs)("tr",{children:[Object(r.jsx)("th",{children:"Rule Number"}),Object(r.jsx)("th",{children:"Port"}),Object(r.jsx)("th",{children:"Protocol"}),Object(r.jsx)("th",{children:"IP Address"}),Object(r.jsx)("th",{children:"Action"})]})}),Object(r.jsx)("tbody",{children:Object.entries(t[n]).map((function(e){var t=Object(c.a)(e,2),s=t[0],i=t[1];return Object(r.jsxs)("tr",{children:[Object(r.jsx)("td",{children:Object(r.jsx)(a.c,{value:s,errorPath:"".concat(n,".").concat(s)})}),Object(r.jsx)("td",{children:Object(r.jsx)(a.c,{value:i.port_range,errorPath:"".concat(n,".").concat(s)})}),Object(r.jsx)("td",{children:Object(r.jsx)(a.c,{value:i.protocol,errorPath:"".concat(n,".").concat(s)})}),Object(r.jsx)("td",{children:Object(r.jsx)(a.c,{value:i.CidrBlock,errorPath:"".concat(n,".").concat(s)})}),Object(r.jsx)("td",{children:Object(r.jsx)(a.c,{value:i.RuleAction,errorPath:"".concat(n,".").concat(s)})})]},s)}))})]})}},562:function(e,t,n){"use strict";n.r(t);var c=n(1),r=(n(0),n(15)),a=n.n(r),s=n(64),i=n.n(s),l=n(103),o=n(640),u=n(645),j=n(642),d=n(516),b=n(646);t.default=function(e){var t=e.data;if(!t)return null;var n=a()(t,["item","rules"]),r=a()(t,["item","Associations"]);return Object(c.jsxs)(o.a,{data:t,children:[Object(c.jsxs)(j.a,{children:[Object(c.jsx)(o.c,{label:"ID",valuePath:"id"}),Object(c.jsx)(o.c,{label:"Default",valuePath:"IsDefault"})]}),Object(c.jsxs)(u.b,{children:[Object(c.jsx)(u.a,{title:"Egress Rules",children:Object(c.jsx)(d.default,{rules:n,type:"egress"})}),Object(c.jsx)(u.a,{title:"Ingress Rules",children:Object(c.jsx)(d.default,{rules:n,type:"ingress"})}),Object(c.jsx)(u.a,{title:"Associated Subnets",children:i()(r)?Object(c.jsx)(o.c,{valuePath:"IsDefault",errorPath:"unused",renderValue:function(e){return!e&&Object(c.jsx)(b.a,{message:"This network ACL is not the VPC's default NACL and is not associated with any existing VPC."})}}):Object(l.l)(r,"SubnetId")})]})]})}},637:function(e,t,n){"use strict";n.d(t,"a",(function(){return s})),n.d(t,"b",(function(){return i})),n.d(t,"c",(function(){return l}));var c=n(0),r=n.n(c),a={path_to_issue:[],item:{}},s=r.a.createContext(a),i=r.a.createContext(""),l=r.a.createContext((function(){}))},638:function(e,t,n){"use strict";var c=n(19),r=n(1),a=n(0),s=n(633),i=n(7),l=n.n(i),o=n(15),u=n.n(o),j=n(10),d=n.n(j),b=n(637),h=n(103),O=n(83),f=(n(641),n(624)),x=n(191),v=n.n(x),p=n(192),m=n(130),P=function(e){var t=e.service,n=e.finding,c=e.path,i=Object(a.useContext)(m.a),l=i.exceptions,o=i.addException,j=Object(p.b)().enqueueSnackbar,d=u()(l,[t,n],[]).includes(c);return Object(r.jsx)(s.a,{title:"Add to exception list",placement:"top",arrow:!0,children:Object(r.jsx)(f.a,{disabled:d,size:"small",startIcon:Object(r.jsx)(v.a,{}),className:"exception-btn",onClick:function(){o(t,n,c),j("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:"Add"})})},g=n(29),C=function(e){var t,n=e.label,i=e.separator,o=e.valuePath,j=e.errorPath,f=e.className,x=e.inline,v=e.tooltip,p=e.tooltipProps,m=e.renderValue,C=e.basePathOverwrite,A=Object(g.g)(),N=Object(a.useContext)(b.a),I=Object(a.useContext)(b.b),k=Object(a.useContext)(b.c),w=Object(h.a)(C||I,o),S=m(e.value||u()(N.item,w,e.value));("boolean"===typeof S&&(S=String(S)),j)?t=(d()(j)?j:[j]).map((function(e){return Object(h.a)(C||I,e)})):t=[w];var y=t.some((function(e){return N.path_to_issues.includes(e)})),D=N.level;if(Object(a.useEffect)((function(){y&&k(D)}),[D]),void 0===S||null===S)return null;var R=Object(r.jsx)(P,{service:A.service,finding:A.finding,path:"".concat(N.path,".").concat(t[0])}),V=Object(r.jsxs)("span",{className:l()(y&&l()("issue",D)),children:[S,y&&R]});return Object(r.jsx)(O.a,{className:l()(f,"partial-value",{inline:x}),label:n,separator:i,value:v?Object(r.jsx)(s.a,Object(c.a)(Object(c.a)({title:S},p),{},{children:V})):V})};C.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=C},639:function(e,t,n){"use strict";var c=n(1),r=n(0),a=n(637),s=n(103);t.a=function(e){var t=e.path,n=e.children,i=Object(r.useContext)(a.b);return Object(c.jsx)(a.b.Provider,{value:Object(s.a)(i,t),children:n})}},640:function(e,t,n){"use strict";n.d(t,"a",(function(){return a})),n.d(t,"b",(function(){return s.a})),n.d(t,"c",(function(){return i.a}));var c=n(1),r=(n(0),n(637)),a=(n(103),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(c.jsx)(r.a.Provider,{value:t,children:n})}),s=n(639),i=n(638)},641:function(e,t,n){},642:function(e,t,n){"use strict";var c=n(1);n(0),n(643);t.a=function(e){var t=e.children;return Object(c.jsxs)("div",{className:"informations-wrapper",children:[Object(c.jsx)("h4",{className:"title",children:"Informations"}),t]})}},643:function(e,t,n){},644:function(e,t,n){},645:function(e,t,n){"use strict";n.d(t,"a",(function(){return j})),n.d(t,"b",(function(){return l.b}));var c=n(1),r=n(18),a=n(0),s=n(7),i=n.n(s),l=n(104),o=n(637),u=n(56),j=(n(644),function(e){var t=e.title,n=e.isSelected,s=e.disabled,j=e.onClick,d=e.children,b=Object(a.useState)(""),h=Object(r.a)(b,2),O=h[0],f=h[1],x=O?Object(c.jsxs)(c.Fragment,{children:[t,u.a[O].icon]}):t;return Object(c.jsx)(o.c.Provider,{value:f,children:Object(c.jsx)(l.a,{title:x,className:i()("partial-tab-pane",O),isSelected:n,disabled:s,onClick:j,children:d})})})},646:function(e,t,n){"use strict";var c=n(1),r=(n(0),n(7)),a=n.n(r),s=n(105),i=n.n(s),l=(n(647),{icon:Object(c.jsx)(i.a,{fontSize:"inherit"})}),o=function(e){var t=e.message,n=e.icon,r=e.className;return Object(c.jsxs)("div",{className:a()("warning-message",r),children:[n,t]})};o.defaultProps=l,t.a=o},647:function(e,t,n){},661:function(e,t,n){}}]);
//# sourceMappingURL=14.8e24a553.chunk.js.map