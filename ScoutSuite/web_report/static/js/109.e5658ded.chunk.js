(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[109],{551:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(697));t.default=function(){return Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)(r.c,{label:"ID",valuePath:"id"}),Object(a.jsx)(r.c,{label:"ARN",valuePath:"arn"}),Object(a.jsx)(r.c,{label:"Region",valuePath:"region"}),Object(a.jsx)(r.c,{label:"State",valuePath:"state"}),Object(a.jsx)(r.c,{label:"CIDR Block",valuePath:"cidr_block"}),Object(a.jsx)(r.c,{label:"Default",valuePath:"default"})]})}},694:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return o})),n.d(t,"c",(function(){return l}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),o=r.a.createContext(""),l=r.a.createContext((function(){}))},695:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(694),i=n(66);t.a=function(e){var t=e.path,n=e.children,o=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(o,t),children:n})}},696:function(e,t,n){"use strict";var a=n(11),r=n(1),c=n(0),i=n(690),o=n(7),l=n.n(o),u=n(13),s=n.n(u),b=n(10),d=n.n(b),j=n(694),v=n(66),f=n(67),p=(n(698),n(686)),h=n(204),x=n.n(h),O=n(699),m=n.n(O),P=n(205),g=n(140),C=function(e){var t=e.service,n=e.finding,a=e.path,o=Object(c.useContext)(g.a),l=o.exceptions,u=o.addException,b=o.removeException,d=Object(P.b)().enqueueSnackbar,j=s()(l,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:j?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(p.a,{size:"small",className:"exception-btn",onClick:j?function(){b(t,n,a),d("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){u(t,n,a),d("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:j?Object(r.jsx)(m.a,{}):Object(r.jsx)(x.a,{})})})},_=n(30),k=function(e){var t,n=e.label,o=e.separator,u=e.valuePath,b=e.errorPath,p=e.className,h=e.inline,x=e.tooltip,O=e.tooltipProps,m=e.renderValue,P=e.basePathOverwrite,g=Object(_.g)(),k=Object(c.useContext)(j.a),A=Object(c.useContext)(j.b),D=Object(c.useContext)(j.c),E=Object(v.a)(P||A,u),R=m(e.value||s()(k.item,E,e.value));("boolean"===typeof R&&(R=String(R)),b)?t=(d()(b)?b:[b]).map((function(e){return Object(v.a)(P||A,e)})):t=[E];var N=t.some((function(e){return k.path_to_issues.includes(e)})),w=k.level;if(Object(c.useEffect)((function(){N&&D(w)}),[w]),void 0===R||null===R)return null;var z=Object(r.jsx)(C,{service:g.service,finding:g.finding,path:"".concat(k.path,".").concat(t[0])}),y=Object(r.jsxs)("span",{className:l()(N&&l()("issue",w)),children:[R,N&&z]});return Object(r.jsx)(f.a,{className:l()(p,"partial-value",{inline:h}),label:n,separator:o,value:x?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:R},O),{},{children:y})):y})};k.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=k},697:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return o.a}));var a=n(1),r=(n(0),n(694)),c=(n(66),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(695),o=n(696)},698:function(e,t,n){},699:function(e,t,n){"use strict";var a=n(35),r=n(37);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var c=r(n(0)),i=(0,a(n(38)).default)(c.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=i}}]);
//# sourceMappingURL=109.e5658ded.chunk.js.map