(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[14,99],{541:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(697));t.default=function(){return Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)(r.c,{label:"Region",valuePath:"region"}),Object(a.jsx)(r.c,{label:"VPC",valuePath:"vpc"}),Object(a.jsx)(r.c,{label:"ID",valuePath:"id"}),Object(a.jsx)(r.c,{label:"Availability Zone",valuePath:"Ec2InstanceAttributes.Ec2AvailabilityZone"}),Object(a.jsx)(r.c,{label:"Status",valuePath:"Status.State"}),Object(a.jsx)(r.c,{label:"Instance Profile",valuePath:"Ec2InstanceAttributes.IamInstanceProfile"}),Object(a.jsx)(r.c,{label:"Visibile to all users",valuePath:"VisibleToAllUsers"})]})}},580:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(13)),c=n.n(r),i=n(29),u=n.n(i),s=n(66),l=n(20),o=n(24),b=n(709),d=n(697),j=n(702),v=n(68),f=n(700),p=n(541);t.default=function(e){var t=e.data,n=c()(t,["item","path"],""),r=Object(b.a)(n),i=Object(b.b)(n),h=Object(l.a)(Object(o.h)("services.ec2.regions.".concat(r,".vpcs.").concat(i))),O=h.data,x=h.loading;if(!t||x)return null;u()(O)||(t.item.vpc="".concat(O.name," (").concat(i,")"),t.item.region=r);var m=c()(t,["item","Ec2InstanceAttributes"]),g=function(e,t){return Object(a.jsx)(v.a,{service:"ec2",resource:"security_groups",id:e,name:t})};return Object(a.jsxs)(d.a,{data:t,children:[Object(a.jsx)(f.a,{children:Object(a.jsx)(p.default,{})}),Object(a.jsxs)(j.b,{children:[Object(a.jsx)(j.a,{title:"Master",children:Object(a.jsxs)("div",{children:[Object(a.jsx)(d.c,{label:"Public DNS",valuePath:"MasterPublicDnsName",renderValue:s.q}),Object(a.jsx)(d.c,{label:"Security Group",value:c()(O,["security_groups",m.EmrManagedMasterSecurityGroup,"name"]),renderValue:function(e){return g(m.EmrManagedMasterSecurityGroup,e)}})]})}),Object(a.jsx)(j.a,{title:"Slave",disabled:u()(m.EmrManagedSlaveSecurityGroup),children:Object(a.jsx)(d.c,{label:"Security Group",value:c()(O,["security_groups",m.EmrManagedSlaveSecurityGroup,"name"]),renderValue:function(e){return g(m.EmrManagedSlaveSecurityGroup,e)}})})]})]})}},694:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return u})),n.d(t,"c",(function(){return s}));var a=n(0),r=n.n(a),c={path_to_issue:[],item:{}},i=r.a.createContext(c),u=r.a.createContext(""),s=r.a.createContext((function(){}))},695:function(e,t,n){"use strict";var a=n(1),r=n(0),c=n(694),i=n(66);t.a=function(e){var t=e.path,n=e.children,u=Object(r.useContext)(c.b);return Object(a.jsx)(c.b.Provider,{value:Object(i.a)(u,t),children:n})}},696:function(e,t,n){"use strict";var a=n(11),r=n(1),c=n(0),i=n(690),u=n(7),s=n.n(u),l=n(13),o=n.n(l),b=n(10),d=n.n(b),j=n(694),v=n(66),f=n(67),p=(n(698),n(686)),h=n(204),O=n.n(h),x=n(699),m=n.n(x),g=n(205),P=n(140),S=function(e){var t=e.service,n=e.finding,a=e.path,u=Object(c.useContext)(P.a),s=u.exceptions,l=u.addException,b=u.removeException,d=Object(g.b)().enqueueSnackbar,j=o()(s,[t,n],[]).includes(a);return Object(r.jsx)(i.a,{title:j?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(p.a,{size:"small",className:"exception-btn",onClick:j?function(){b(t,n,a),d("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){l(t,n,a),d("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:j?Object(r.jsx)(m.a,{}):Object(r.jsx)(O.a,{})})})},y=n(30),E=function(e){var t,n=e.label,u=e.separator,l=e.valuePath,b=e.errorPath,p=e.className,h=e.inline,O=e.tooltip,x=e.tooltipProps,m=e.renderValue,g=e.basePathOverwrite,P=Object(y.g)(),E=Object(c.useContext)(j.a),C=Object(c.useContext)(j.b),A=Object(c.useContext)(j.c),M=Object(v.a)(g||C,l),I=m(e.value||o()(E.item,M,e.value));("boolean"===typeof I&&(I=String(I)),b)?t=(d()(b)?b:[b]).map((function(e){return Object(v.a)(g||C,e)})):t=[M];var N=t.some((function(e){return E.path_to_issues.includes(e)})),_=E.level;if(Object(c.useEffect)((function(){N&&A(_)}),[_]),void 0===I||null===I)return null;var V=Object(r.jsx)(S,{service:P.service,finding:P.finding,path:"".concat(E.path,".").concat(t[0])}),G=Object(r.jsxs)("span",{className:s()(N&&s()("issue",_)),children:[I,N&&V]});return Object(r.jsx)(f.a,{className:s()(p,"partial-value",{inline:h}),label:n,separator:u,value:O?Object(r.jsx)(i.a,Object(a.a)(Object(a.a)({title:I},x),{},{children:G})):G})};E.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=E},697:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i.a})),n.d(t,"c",(function(){return u.a}));var a=n(1),r=(n(0),n(694)),c=(n(66),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),i=n(695),u=n(696)},698:function(e,t,n){},699:function(e,t,n){"use strict";var a=n(35),r=n(37);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var c=r(n(0)),i=(0,a(n(38)).default)(c.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=i},700:function(e,t,n){"use strict";var a=n(1);n(0),n(701);t.a=function(e){var t=e.children;return Object(a.jsxs)("div",{className:"informations-wrapper",children:[Object(a.jsx)("h4",{className:"title",children:"Informations"}),t]})}},701:function(e,t,n){},702:function(e,t,n){"use strict";n.d(t,"a",(function(){return b})),n.d(t,"b",(function(){return s.b}));var a=n(1),r=n(18),c=n(0),i=n(7),u=n.n(i),s=n(114),l=n(694),o=n(58),b=(n(703),function(e){var t=e.title,n=e.isSelected,i=e.disabled,b=e.onClick,d=e.children,j=Object(c.useState)(""),v=Object(r.a)(j,2),f=v[0],p=v[1],h=f?Object(a.jsxs)(a.Fragment,{children:[t,o.a[f].icon]}):t;return Object(a.jsx)(l.c.Provider,{value:p,children:Object(a.jsx)(s.a,{title:h,className:u()("partial-tab-pane",f),isSelected:n,disabled:i,onClick:b,children:d})})})},703:function(e,t,n){},709:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return i}));var a=n(13),r=n.n(a),c=function(e){return r()(e.match(/regions\.([^.]*)/),1)},i=function(e){return r()(e.match(/vpcs\.([^.]*)/),1)}}}]);
//# sourceMappingURL=14.7e0e6f6e.chunk.js.map