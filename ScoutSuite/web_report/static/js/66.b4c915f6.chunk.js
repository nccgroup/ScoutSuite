(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[66],{660:function(e,t,n){"use strict";n.r(t);var a=n(1),r=n(15),c=(n(0),n(739)),i=n(91),s=n(126),l=n(16),o=n.n(l),u=n(742),j=function(e){var t=Object.entries(e);return Object(a.jsx)("ul",{children:t.map((function(e){var t=Object(r.a)(e,2),n=t[0],i=t[1];return Object(a.jsxs)("li",{children:[Object(a.jsx)(c.c,{errorPath:n,value:n}),Object(a.jsxs)("ul",{children:[i.map((function(e,t){return Object(a.jsx)("li",{children:Object(a.jsx)(c.c,{errorPath:"".concat(n,".").concat(t,".permissive_ports"),value:e})},t)})),0===i.length&&Object(a.jsx)("li",{children:"None"})]})]},n)}))})},b=function(e){return Object(a.jsx)("ul",{children:e.map((function(e,t){return Object(a.jsx)("li",{children:e},t)}))})};t.default=function(e){var t=e.data;if(!t)return null;var n=o()(t,["item"],{});return Object(a.jsxs)(c.a,{data:t,children:[Object(a.jsxs)(u.a,{children:[Object(a.jsx)(c.c,{label:"Firewall name",valuePath:"name"}),Object(a.jsx)(c.c,{label:"Project ID",valuePath:"project_id"}),Object(a.jsx)(c.c,{label:"Description",valuePath:"description"}),Object(a.jsx)(c.c,{label:"Network",valuePath:"network"}),Object(a.jsx)(c.c,{label:"Creation Date",valuePath:"creation_timestamp",renderValue:i.h}),Object(a.jsx)(c.c,{label:"Priority",valuePath:"priority"}),Object(a.jsx)(c.c,{label:"Disabled",valuePath:"disabled",renderValue:i.d})]}),Object(a.jsxs)(s.b,{children:[Object(a.jsx)(s.a,{title:"Configuration",children:Object(a.jsxs)("div",{children:[Object(a.jsx)(c.c,{label:"Direction",valuePath:"direction"}),Object(a.jsx)(c.c,{label:"Action",valuePath:"action"}),n.source_ranges&&Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)(c.c,{errorPath:"source_ranges",value:"Source Ranges:"}),b(n.source_ranges)]}),n.destination_ranges&&Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)(c.c,{errorPath:"destination_ranges",value:"Destination Ranges:"}),b(n.source_ranges)]}),n.source_tags&&Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)(c.c,{errorPath:"source_tags",value:"Source Tags:"}),b(n.source_tags)]}),n.target_tags&&Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)(c.c,{errorPath:"target_tags",value:"Target Tags:"}),b(n.target_tags)]})]})}),"allowed"===n.action&&Object(a.jsx)(s.a,{title:"Allowed Traffic",children:Object(a.jsx)(c.b,{path:"allowed_traffic",children:j(n.allowed_traffic)})}),"allowed"!==n.action&&Object(a.jsx)(s.a,{title:"Denied Traffic",children:Object(a.jsx)(c.b,{path:"denied_traffic",children:j(n.denied_traffic)})})]})]})}},736:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return s})),n.d(t,"c",(function(){return l}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),s=r.a.createContext(""),l=r.a.createContext((function(){}))},737:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(736),i=n(91);t.a=function(e){var t=e.path,n=e.children,s=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(s,t),children:n})}},738:function(e,t,n){"use strict";var a=n(13),r=n(1),c=n(0),i=n(732),s=n(9),l=n.n(s),o=n(16),u=n.n(o),j=n(14),b=n.n(j),d=n(736),h=n(91),f=n(71),v=(n(740),n(723)),O=n(216),x=n.n(O),p=n(741),g=n.n(p),m=n(217),P=n(151),_=function(e){var t=e.service,n=e.finding,a=e.path,s=Object(c.useContext)(P.a),l=s.exceptions,o=s.addException,j=s.removeException,b=Object(m.b)().enqueueSnackbar,d=u()(l,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:d?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(v.a,{size:"small",className:"exception-btn",onClick:d?function(){j(t,n,a),b("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){o(t,n,a),b("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:d?Object(r.jsx)(g.a,{}):Object(r.jsx)(x.a,{})})})},w=n(34),C=function(e){var t,n=e.label,s=e.separator,o=e.valuePath,j=e.errorPath,v=e.className,O=e.inline,x=e.tooltip,p=e.tooltipProps,g=e.renderValue,m=e.basePathOverwrite,P=Object(w.g)(),C=Object(c.useContext)(d.a),D=Object(c.useContext)(d.b),N=Object(c.useContext)(d.c),A=Object(h.a)(m||D,o),T=g(e.value||u()(C.item,A,e.value));("boolean"===typeof T&&(T=String(T)),j)?t=(b()(j)?j:[j]).map((function(e){return Object(h.a)(m||D,e)})):t=[A];var k=t.some((function(e){return C.path_to_issues.includes(e)})),E=C.level;if(Object(c.useEffect)((function(){k&&N(E)}),[E]),void 0===T||null===T)return null;var y=Object(r.jsx)(_,{service:P.service,finding:P.finding,path:"".concat(C.path,".").concat(t[0])}),F=Object(r.jsxs)("span",{className:l()(k&&l()("issue",E)),children:[T,k&&y]});return Object(r.jsx)(f.a,{className:l()(v,"partial-value",{inline:O}),label:n,separator:s,value:x?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:T},p),{},{children:F})):F})};C.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=C},739:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return s.a}));var a=n(1),r=(n(0),n(736)),c=(n(91),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(737),s=n(738)},740:function(e,t,n){},741:function(e,t,n){"use strict";var a=n(36),r=n(38);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var c=r(n(0)),i=(0,a(n(39)).default)(c.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=i},742:function(e,t,n){"use strict";var a=n(1);n(0),n(743);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},743:function(e,t,n){}}]);
//# sourceMappingURL=66.b4c915f6.chunk.js.map