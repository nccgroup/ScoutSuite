(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[63],{633:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(700)),i=n(697),c=n(66);t.default=function(e){var t=e.data;return t?Object(a.jsx)(i.a,{data:t,children:Object(a.jsxs)(r.a,{children:[Object(a.jsx)(i.c,{label:"Name",valuePath:"name",renderValue:c.q}),Object(a.jsx)(i.c,{label:"Provisioning State",valuePath:"provisioning_state",renderValue:c.q}),Object(a.jsx)(i.c,{label:"Location",valuePath:"location",renderValue:c.q}),Object(a.jsx)(i.c,{label:"Hyper-V Generation",valuePath:"hyper_vgeneration",renderValue:c.q})]})}):null}},694:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return o})),n.d(t,"c",(function(){return l}));var a=n(0),r=n.n(a),i={path_to_issue:[],item:{}},c=r.a.createContext(i),o=r.a.createContext(""),l=r.a.createContext((function(){}))},695:function(e,t,n){"use strict";var a=n(1),r=n(0),i=n(694),c=n(66);t.a=function(e){var t=e.path,n=e.children,o=Object(r.useContext)(i.b);return Object(a.jsx)(i.b.Provider,{value:Object(c.a)(o,t),children:n})}},696:function(e,t,n){"use strict";var a=n(11),r=n(1),i=n(0),c=n(690),o=n(7),l=n.n(o),s=n(13),u=n.n(s),d=n(10),b=n.n(d),v=n(694),f=n(66),j=n(67),p=(n(698),n(686)),h=n(204),x=n.n(h),O=n(699),m=n.n(O),P=n(205),g=n(140),C=function(e){var t=e.service,n=e.finding,a=e.path,o=Object(i.useContext)(g.a),l=o.exceptions,s=o.addException,d=o.removeException,b=Object(P.b)().enqueueSnackbar,v=u()(l,[t,n],[]).includes(a);return Object(r.jsx)(c.a,{title:v?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(p.a,{size:"small",className:"exception-btn",onClick:v?function(){d(t,n,a),b("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){s(t,n,a),b("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:v?Object(r.jsx)(m.a,{}):Object(r.jsx)(x.a,{})})})},_=n(30),N=function(e){var t,n=e.label,o=e.separator,s=e.valuePath,d=e.errorPath,p=e.className,h=e.inline,x=e.tooltip,O=e.tooltipProps,m=e.renderValue,P=e.basePathOverwrite,g=Object(_.g)(),N=Object(i.useContext)(v.a),V=Object(i.useContext)(v.b),E=Object(i.useContext)(v.c),q=Object(f.a)(P||V,s),w=m(e.value||u()(N.item,q,e.value));("boolean"===typeof w&&(w=String(w)),d)?t=(b()(d)?d:[d]).map((function(e){return Object(f.a)(P||V,e)})):t=[q];var y=t.some((function(e){return N.path_to_issues.includes(e)})),A=N.level;if(Object(i.useEffect)((function(){y&&E(A)}),[A]),void 0===w||null===w)return null;var k=Object(r.jsx)(C,{service:g.service,finding:g.finding,path:"".concat(N.path,".").concat(t[0])}),z=Object(r.jsxs)("span",{className:l()(y&&l()("issue",A)),children:[w,y&&k]});return Object(r.jsx)(j.a,{className:l()(p,"partial-value",{inline:h}),label:n,separator:o,value:x?Object(r.jsx)(c.a,Object(a.a)(Object(a.a)({title:w},O),{},{children:z})):z})};N.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=N},697:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return c.a})),n.d(t,"c",(function(){return o.a}));var a=n(1),r=(n(0),n(694)),i=(n(66),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),c=n(695),o=n(696)},698:function(e,t,n){},699:function(e,t,n){"use strict";var a=n(35),r=n(37);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var i=r(n(0)),c=(0,a(n(38)).default)(i.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=c},700:function(e,t,n){"use strict";var a=n(1);n(0),n(701);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},701:function(e,t,n){}}]);
//# sourceMappingURL=63.7e9dc61b.chunk.js.map