(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[62],{654:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(742)),c=n(739),i=n(91);t.default=function(e){var t=e.data;return t?Object(a.jsx)(c.a,{data:t,children:Object(a.jsxs)(r.a,{children:[Object(a.jsx)(c.c,{label:"Name",valuePath:"name",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Unique ID",valuePath:"unique_id",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Location",valuePath:"location",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Time Created",valuePath:"time_created",renderValue:i.h}),Object(a.jsx)(c.c,{label:"Provisioning State",valuePath:"provisioning_state",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Disk State",valuePath:"disk_state",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Zones",valuePath:"zones",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Encryption Type",valuePath:"encryption_type",renderValue:i.q}),Object(a.jsx)(c.c,{label:"OS Type",valuePath:"os_type",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Hyper V Generation",valuePath:"hyper_vgeneration",renderValue:i.q}),Object(a.jsx)(c.c,{label:"Disk Size GB",valuePath:"disk_size_gb",renderValue:i.q})]})}):null}},736:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return l})),n.d(t,"c",(function(){return o}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),l=r.a.createContext(""),o=r.a.createContext((function(){}))},737:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(736),i=n(91);t.a=function(e){var t=e.path,n=e.children,l=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(l,t),children:n})}},738:function(e,t,n){"use strict";var a=n(13),r=n(1),c=n(0),i=n(732),l=n(9),o=n.n(l),u=n(16),s=n.n(u),d=n(14),b=n.n(d),j=n(736),v=n(91),p=n(71),f=(n(740),n(723)),h=n(216),x=n.n(h),O=n(741),m=n.n(O),P=n(217),g=n(151),_=function(e){var t=e.service,n=e.finding,a=e.path,l=Object(c.useContext)(g.a),o=l.exceptions,u=l.addException,d=l.removeException,b=Object(P.b)().enqueueSnackbar,j=s()(o,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:j?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(f.a,{size:"small",className:"exception-btn",onClick:j?function(){d(t,n,a),b("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){u(t,n,a),b("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:j?Object(r.jsx)(m.a,{}):Object(r.jsx)(x.a,{})})})},V=n(34),q=function(e){var t,n=e.label,l=e.separator,u=e.valuePath,d=e.errorPath,f=e.className,h=e.inline,x=e.tooltip,O=e.tooltipProps,m=e.renderValue,P=e.basePathOverwrite,g=Object(V.g)(),q=Object(c.useContext)(j.a),y=Object(c.useContext)(j.b),C=Object(c.useContext)(j.c),k=Object(v.a)(P||y,u),z=m(e.value||s()(q.item,k,e.value));("boolean"===typeof z&&(z=String(z)),d)?t=(b()(d)?d:[d]).map((function(e){return Object(v.a)(P||y,e)})):t=[k];var E=t.some((function(e){return q.path_to_issues.includes(e)})),N=q.level;if(Object(c.useEffect)((function(){E&&C(N)}),[N]),void 0===z||null===z)return null;var D=Object(r.jsx)(_,{service:g.service,finding:g.finding,path:"".concat(q.path,".").concat(t[0])}),S=Object(r.jsxs)("span",{className:o()(E&&o()("issue",N)),children:[z,E&&D]});return Object(r.jsx)(p.a,{className:o()(f,"partial-value",{inline:h}),label:n,separator:l,value:x?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:z},O),{},{children:S})):S})};q.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=q},739:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return l.a}));var a=n(1),r=(n(0),n(736)),c=(n(91),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(737),l=n(738)},740:function(e,t,n){},741:function(e,t,n){"use strict";var a=n(36),r=n(38);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var c=r(n(0)),i=(0,a(n(39)).default)(c.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=i},742:function(e,t,n){"use strict";var a=n(1);n(0),n(743);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},743:function(e,t,n){}}]);
//# sourceMappingURL=62.46101ff0.chunk.js.map