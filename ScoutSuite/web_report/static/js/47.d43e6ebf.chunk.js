(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[47],{502:function(e,t,n){"use strict";n.r(t);var c=n(1),r=n(18),a=n(0),s=n(15),o=n.n(s),i=n(637),u=n(640),l=n(646);n(657);t.default=function(){var e=Object(a.useContext)(i.a),t=Object(a.useContext)(i.b),n=o()(e.item,t),s="default"===o()(e.item,"name"),j=function(e,t,n){return Object(c.jsxs)("li",{children:["".concat(e,":"),Object(c.jsx)("ul",{children:t.map((function(e,t){return Object(c.jsx)("li",{children:Object(c.jsx)(u.c,{value:e,errorPath:n,renderValue:function(e){return e.CIDRName?"".concat(e.CIDR," (").concat(e.CIDRName,")"):e.CIDR}})},t)}))})]})};return Object(c.jsxs)(c.Fragment,{children:[Object(c.jsx)("ul",{className:"rules-list",children:Object.entries(n.protocols).map((function(e,t){var n=Object(r.a)(e,2),a=n[0],s=n[1].ports;return Object(c.jsxs)("div",{children:[Object(c.jsx)("li",{children:a}),Object(c.jsx)("ul",{children:Object(c.jsxs)("li",{children:["Ports:",Object(c.jsx)("ul",{children:Object.entries(s).map((function(e,t){var n,s,o=Object(r.a)(e,2),i=o[0],l=o[1];return Object(c.jsxs)("div",{children:[Object(c.jsx)("li",{children:Object(c.jsx)(u.c,{value:i,errorPath:"protocols.".concat(a,".ports.").concat(i)})}),Object(c.jsxs)("ul",{children:[l.cidrs&&j("IP adresses",l.cidrs,"protocols.".concat(a,".ports.").concat(i,".cidrs.").concat(t,".CIDR")),l.Ipv6Ranges&&j("IPv6 addresses",l.Ipv6Ranges,"protocols.".concat(a,".ports.").concat(i,".cidrs.").concat(t,".CIDR")),l.security_groups&&(n=l.security_groups,s="protocols.".concat(a,".ports.").concat(i,".security_groups.").concat(t),Object(c.jsxs)("li",{children:["EC2 security groups:",Object(c.jsx)("ul",{children:n.map((function(e,t){return Object(c.jsx)("li",{children:Object(c.jsx)(u.c,{value:e,errorPath:s,renderValue:function(e){return e.GroupName?"".concat(e.GroupName," (").concat(e.GroupId,")"):"".concat(e.GroupId," (AWS Account ID: ").concat(e.UserId,")")}})},t)}))})]}))]})]},t)}))})]})})]},t)}))}),s&&Object(c.jsx)(u.c,{errorPath:"default_with_rules",renderValue:function(){return Object(c.jsx)(l.a,{className:"rules-list__warning-message",message:"Default security groups should have no rules."})}})]})}},637:function(e,t,n){"use strict";n.d(t,"a",(function(){return s})),n.d(t,"b",(function(){return o})),n.d(t,"c",(function(){return i}));var c=n(0),r=n.n(c),a={path_to_issue:[],item:{}},s=r.a.createContext(a),o=r.a.createContext(""),i=r.a.createContext((function(){}))},638:function(e,t,n){"use strict";var c=n(19),r=n(1),a=n(0),s=n(633),o=n(7),i=n.n(o),u=n(15),l=n.n(u),j=n(10),d=n.n(j),b=n(637),p=n(103),f=n(83),O=(n(641),n(624)),h=n(191),x=n.n(h),v=n(192),m=n(130),g=function(e){var t=e.service,n=e.finding,c=e.path,o=Object(a.useContext)(m.a),i=o.exceptions,u=o.addException,j=Object(v.b)().enqueueSnackbar,d=l()(i,[t,n],[]).includes(c);return Object(r.jsx)(s.a,{title:"Add to exception list",placement:"top",arrow:!0,children:Object(r.jsx)(O.a,{disabled:d,size:"small",startIcon:Object(r.jsx)(x.a,{}),className:"exception-btn",onClick:function(){u(t,n,c),j("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:"Add"})})},P=n(29),C=function(e){var t,n=e.label,o=e.separator,u=e.valuePath,j=e.errorPath,O=e.className,h=e.inline,x=e.tooltip,v=e.tooltipProps,m=e.renderValue,C=e.basePathOverwrite,I=Object(P.g)(),N=Object(a.useContext)(b.a),D=Object(a.useContext)(b.b),_=Object(a.useContext)(b.c),R=Object(p.a)(C||D,u),A=m(e.value||l()(N.item,R,e.value));("boolean"===typeof A&&(A=String(A)),j)?t=(d()(j)?j:[j]).map((function(e){return Object(p.a)(C||D,e)})):t=[R];var w=t.some((function(e){return N.path_to_issues.includes(e)})),y=N.level;if(Object(a.useEffect)((function(){w&&_(y)}),[y]),void 0===A||null===A)return null;var V=Object(r.jsx)(g,{service:I.service,finding:I.finding,path:"".concat(N.path,".").concat(t[0])}),k=Object(r.jsxs)("span",{className:i()(w&&i()("issue",y)),children:[A,w&&V]});return Object(r.jsx)(f.a,{className:i()(O,"partial-value",{inline:h}),label:n,separator:o,value:x?Object(r.jsx)(s.a,Object(c.a)(Object(c.a)({title:A},v),{},{children:k})):k})};C.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=C},639:function(e,t,n){"use strict";var c=n(1),r=n(0),a=n(637),s=n(103);t.a=function(e){var t=e.path,n=e.children,o=Object(r.useContext)(a.b);return Object(c.jsx)(a.b.Provider,{value:Object(s.a)(o,t),children:n})}},640:function(e,t,n){"use strict";n.d(t,"a",(function(){return a})),n.d(t,"b",(function(){return s.a})),n.d(t,"c",(function(){return o.a}));var c=n(1),r=(n(0),n(637)),a=(n(103),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(c.jsx)(r.a.Provider,{value:t,children:n})}),s=n(639),o=n(638)},641:function(e,t,n){},646:function(e,t,n){"use strict";var c=n(1),r=(n(0),n(7)),a=n.n(r),s=n(105),o=n.n(s),i=(n(647),{icon:Object(c.jsx)(o.a,{fontSize:"inherit"})}),u=function(e){var t=e.message,n=e.icon,r=e.className;return Object(c.jsxs)("div",{className:a()("warning-message",r),children:[n,t]})};u.defaultProps=i,t.a=u},647:function(e,t,n){},657:function(e,t,n){}}]);
//# sourceMappingURL=47.d43e6ebf.chunk.js.map