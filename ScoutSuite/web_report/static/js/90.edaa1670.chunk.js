(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[90],{585:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(91)),c=n(739);t.default=function(e){var t=e.data;return t?Object(a.jsx)(c.a,{data:t,children:Object(a.jsxs)("div",{children:[Object(a.jsx)("h4",{children:"Informations"}),Object(a.jsx)(c.c,{label:"Name",valuePath:"name",renderValue:r.q}),Object(a.jsx)(c.c,{label:"Creation Time",valuePath:"creation_time",renderValue:r.h}),Object(a.jsx)(c.c,{label:"Log Group Name",valuePath:"log_group_name",renderValue:r.q}),Object(a.jsx)(c.c,{label:"Pattern",valuePath:"pattern",renderValue:function(e){return Object(a.jsx)("code",{children:Object(r.q)(e)})}})]})}):null}},736:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return o})),n.d(t,"c",(function(){return l}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),o=r.a.createContext(""),l=r.a.createContext((function(){}))},737:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(736),i=n(91);t.a=function(e){var t=e.path,n=e.children,o=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(o,t),children:n})}},738:function(e,t,n){"use strict";var a=n(13),r=n(1),c=n(0),i=n(732),o=n(9),l=n.n(o),u=n(16),s=n.n(u),d=n(14),b=n.n(d),j=n(736),v=n(91),f=n(71),p=(n(740),n(723)),h=n(216),x=n.n(h),O=n(741),m=n.n(O),P=n(217),g=n(151),C=function(e){var t=e.service,n=e.finding,a=e.path,o=Object(c.useContext)(g.a),l=o.exceptions,u=o.addException,d=o.removeException,b=Object(P.b)().enqueueSnackbar,j=s()(l,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:j?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(p.a,{size:"small",className:"exception-btn",onClick:j?function(){d(t,n,a),b("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){u(t,n,a),b("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:j?Object(r.jsx)(m.a,{}):Object(r.jsx)(x.a,{})})})},_=n(34),E=function(e){var t,n=e.label,o=e.separator,u=e.valuePath,d=e.errorPath,p=e.className,h=e.inline,x=e.tooltip,O=e.tooltipProps,m=e.renderValue,P=e.basePathOverwrite,g=Object(_.g)(),E=Object(c.useContext)(j.a),N=Object(c.useContext)(j.b),V=Object(c.useContext)(j.c),A=Object(v.a)(P||N,u),k=m(e.value||s()(E.item,A,e.value));("boolean"===typeof k&&(k=String(k)),d)?t=(b()(d)?d:[d]).map((function(e){return Object(v.a)(P||N,e)})):t=[A];var q=t.some((function(e){return E.path_to_issues.includes(e)})),w=E.level;if(Object(c.useEffect)((function(){q&&V(w)}),[w]),void 0===k||null===k)return null;var z=Object(r.jsx)(C,{service:g.service,finding:g.finding,path:"".concat(E.path,".").concat(t[0])}),y=Object(r.jsxs)("span",{className:l()(q&&l()("issue",w)),children:[k,q&&z]});return Object(r.jsx)(f.a,{className:l()(p,"partial-value",{inline:h}),label:n,separator:o,value:x?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:k},O),{},{children:y})):y})};E.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=E},739:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return o.a}));var a=n(1),r=(n(0),n(736)),c=(n(91),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(737),o=n(738)},740:function(e,t,n){},741:function(e,t,n){"use strict";var a=n(36),r=n(38);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var c=r(n(0)),i=(0,a(n(39)).default)(c.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=i}}]);
//# sourceMappingURL=90.edaa1670.chunk.js.map