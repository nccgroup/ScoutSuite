(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[9],{666:function(e,t,n){"use strict";n.r(t);var r=n(1),i=(n(0),n(766)),s=n(55),o=n(44),a=n(769),c=n(64),l=n(776),u=n(771),p=function(e){return Object(o.l)(e,"",(function(e){return function(e){return Object(r.jsx)(c.a,{service:"aad",resource:"groups",id:e.id,name:e.name})}(e)}))},g=function(e){return Object(o.l)(e,"",(function(e){return function(e){return Object(r.jsx)(c.a,{service:"aad",resource:"users",id:e.id,name:e.name})}(e)}))},h=function(e){return Object(o.l)(e,"",(function(e){return function(e){return Object(r.jsx)(c.a,{service:"aad",resource:"service_principals",id:e.id,name:e.name})}(e)}))};t.default=function(e){var t=e.data,n=e.item,c=Object(l.a)("aad","users",n.assignments?n.assignments.users:[]).data,f=Object(l.a)("aad","groups",n.assignments?n.assignments.groups:[]).data,d=Object(l.a)("aad","service_principals",n.assignments?n.assignments.service_principals:[]).data;return t?Object(r.jsxs)(s.a,{data:t,children:[Object(r.jsxs)(i.a,{children:[Object(r.jsx)(s.c,{label:"ID",valuePath:"id",renderValue:o.q}),Object(r.jsx)(s.c,{label:"Description",valuePath:"description",renderValue:o.q}),Object(r.jsx)(s.c,{label:"Type",valuePath:"type",renderValue:o.q}),Object(r.jsx)(s.c,{label:"Role Type",valuePath:"role_type",renderValue:o.q}),Object(r.jsx)(s.c,{label:"Assignable Scopes",valuePath:"assignable_scopes",renderValue:o.q}),Object(r.jsx)(s.c,{label:"Custom Subscriptions Owner Roles",valuePath:"custom_subscription_owner_role"})]}),Object(r.jsxs)(a.b,{children:[Object(r.jsx)(a.a,{title:"Permissions",children:Object(r.jsx)(u.a,{name:"",policy:n.permissions,defaultOpen:!0})}),Object(r.jsxs)(a.a,{title:"Assignments",children:[n.assignments.users&&Object(r.jsxs)(r.Fragment,{children:[Object(r.jsx)(s.c,{label:"Users",errorPath:"users",value:""}),Object(r.jsx)("ul",{children:g(c)})]}),n.assignments.groups&&Object(r.jsxs)(r.Fragment,{children:[Object(r.jsx)(s.c,{label:"Groups",errorPath:"groups",value:""}),Object(r.jsx)("ul",{children:p(f)})]}),n.assignments.service_principals&&Object(r.jsxs)(r.Fragment,{children:[Object(r.jsx)(s.c,{label:"Service Principals",errorPath:"serviceprincipals",value:""}),Object(r.jsx)("ul",{children:h(d)})]})]})]})]}):null}},766:function(e,t,n){"use strict";var r=n(1);n(0),n(767);t.a=function(e){var t=e.children;return Object(r.jsxs)("div",{className:"informations-wrapper",children:[Object(r.jsx)("h4",{className:"title",children:"Informations"}),t]})}},767:function(e,t,n){},768:function(e,t,n){},769:function(e,t,n){"use strict";n.d(t,"a",(function(){return p})),n.d(t,"b",(function(){return c.b}));var r=n(1),i=n(13),s=n(0),o=n(8),a=n.n(o),c=n(79),l=n(80),u=n(63),p=(n(768),function(e){var t=e.title,n=e.isSelected,o=e.disabled,p=e.onClick,g=e.children,h=Object(s.useState)(""),f=Object(i.a)(h,2),d=f[0],b=f[1],m=d?Object(r.jsxs)(r.Fragment,{children:[t,u.a[d].icon]}):t;return Object(r.jsx)(l.c.Provider,{value:b,children:Object(r.jsx)(c.a,{title:m,className:a()("partial-tab-pane",d),isSelected:n,disabled:o,onClick:p,children:g})})})},770:function(e,t,n){"use strict";var r=n(37),i=n(39);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=i(n(0)),o=(0,r(n(40)).default)(s.createElement("path",{d:"M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"}),"ExpandMore");t.default=o},771:function(e,t,n){"use strict";var r=n(1),i=n(13),s=n(0),o=n(8),a=n.n(o),c=n(772),l=n.n(c),u=n(770),p=n.n(u),g=n(774),h=n.n(g),f=n(159),d=n.n(f),b=n(29),m=n.n(b),O=n(80),j=n(227),v=n(44),y=(n(773),function(e){var t=e.name,n=e.policy,o=e.policyPath,c=e.defaultOpen,u=Object(s.useContext)(O.a).path_to_issues.some((function(e){return e.includes(o)}));if(m()(n))return null;var g=Object(r.jsx)("h4",{className:"policy-title",children:t}),f=function(e,t){return Object(r.jsx)(j.a,{value:(n=e,JSON.stringify(n,null,2).replace(/ /gm,"&nbsp;").replace(/\n/gm,"<br/>")),errorPath:t,renderValue:function(e){return Object(v.p)(e)}});var n},b=Object(r.jsxs)("code",{children:["{",Object.entries(n).map((function(e,t){var s=Object(i.a)(e,2),c=s[0],u=s[1];return Object(r.jsxs)("div",{className:a()({inline:"string"===typeof u}),children:['"'.concat(c,'":\xa0'),"Statement"===c?Object(r.jsxs)(r.Fragment,{children:["[",Object(r.jsx)("br",{}),u.map((function(e,t){return Object(r.jsx)(l.a,{trigger:Object(r.jsxs)(r.Fragment,{children:[Object(r.jsx)(p.a,{fontSize:"inherit"}),Object(r.jsx)("span",{children:"{...}"})]}),triggerWhenOpen:Object(r.jsx)(h.a,{fontSize:"inherit"}),transitionTime:1,open:!0,children:f(e,"".concat(o,".Statement.").concat(t))},t)})),"]"]}):Object(r.jsx)(r.Fragment,{children:f(u)}),t<d()(n)-1&&",",Object(r.jsx)("br",{})]},t)})),"}"]});return Object(r.jsx)("div",{className:"policy",children:t?Object(r.jsx)(l.a,{trigger:Object(r.jsxs)(r.Fragment,{children:[g,Object(r.jsx)(p.a,{fontSize:"inherit"})]}),triggerWhenOpen:Object(r.jsxs)(r.Fragment,{children:[g,Object(r.jsx)(h.a,{fontSize:"inherit"})]}),transitionTime:1,open:c||u,children:b}):b})});y.defaultProps={defaultOpen:!1},t.a=y},772:function(e,t,n){var r;e.exports=(r=n(0),function(e){var t={};function n(r){if(t[r])return t[r].exports;var i=t[r]={i:r,l:!1,exports:{}};return e[r].call(i.exports,i,i.exports,n),i.l=!0,i.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)n.d(r,i,function(t){return e[t]}.bind(null,i));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=4)}([function(e,t,n){e.exports=n(2)()},function(e,t){e.exports=r},function(e,t,n){"use strict";var r=n(3);function i(){}function s(){}s.resetWarningCache=i,e.exports=function(){function e(e,t,n,i,s,o){if(o!==r){var a=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw a.name="Invariant Violation",a}}function t(){return e}e.isRequired=e;var n={array:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:t,element:e,elementType:e,instanceOf:t,node:e,objectOf:t,oneOf:t,oneOfType:t,shape:t,exact:t,checkPropTypes:s,resetWarningCache:i};return n.PropTypes=n,n}},function(e,t,n){"use strict";e.exports="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED"},function(e,t,n){"use strict";n.r(t);var r=n(1),i=n.n(r),s=n(0),o=n.n(s),a=function(e){return 0!==e};function c(e){return(c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function l(){return(l=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function u(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function p(e,t){return(p=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function g(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=d(e);if(t){var i=d(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return h(this,n)}}function h(e,t){return!t||"object"!==c(t)&&"function"!=typeof t?f(e):t}function f(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function d(e){return(d=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function b(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var m=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&p(e,t)}(o,e);var t,n,r,s=g(o);function o(e){var t;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,o),b(f(t=s.call(this,e)),"continueOpenCollapsible",(function(){var e=f(t).innerRef;t.setState({height:e.scrollHeight,transition:"height ".concat(t.props.transitionTime,"ms ").concat(t.props.easing),isClosed:!1,hasBeenOpened:!0,inTransition:a(e.scrollHeight),shouldOpenOnNextCycle:!1})})),b(f(t),"handleTriggerClick",(function(e){t.props.triggerDisabled||t.state.inTransition||(e.preventDefault(),t.props.handleTriggerClick?t.props.handleTriggerClick(t.props.accordionPosition):!0===t.state.isClosed?(t.openCollapsible(),t.props.onOpening(),t.props.onTriggerOpening()):(t.closeCollapsible(),t.props.onClosing(),t.props.onTriggerClosing()))})),b(f(t),"handleTransitionEnd",(function(e){e.target===t.innerRef&&(t.state.isClosed?(t.setState({inTransition:!1}),t.props.onClose()):(t.setState({height:"auto",overflow:t.props.overflowWhenOpen,inTransition:!1}),t.props.onOpen()))})),b(f(t),"setInnerRef",(function(e){return t.innerRef=e})),t.timeout=void 0,e.open?t.state={isClosed:!1,shouldSwitchAutoOnNextCycle:!1,height:"auto",transition:"none",hasBeenOpened:!0,overflow:e.overflowWhenOpen,inTransition:!1}:t.state={isClosed:!0,shouldSwitchAutoOnNextCycle:!1,height:0,transition:"height ".concat(e.transitionTime,"ms ").concat(e.easing),hasBeenOpened:!1,overflow:"hidden",inTransition:!1},t}return t=o,(n=[{key:"componentDidUpdate",value:function(e,t){var n=this;this.state.shouldOpenOnNextCycle&&this.continueOpenCollapsible(),"auto"!==t.height&&0!==t.height||!0!==this.state.shouldSwitchAutoOnNextCycle||(window.clearTimeout(this.timeout),this.timeout=window.setTimeout((function(){n.setState({height:0,overflow:"hidden",isClosed:!0,shouldSwitchAutoOnNextCycle:!1})}),50)),e.open!==this.props.open&&(!0===this.props.open?(this.openCollapsible(),this.props.onOpening()):(this.closeCollapsible(),this.props.onClosing()))}},{key:"componentWillUnmount",value:function(){window.clearTimeout(this.timeout)}},{key:"closeCollapsible",value:function(){var e=this.innerRef;this.setState({shouldSwitchAutoOnNextCycle:!0,height:e.scrollHeight,transition:"height ".concat(this.props.transitionCloseTime?this.props.transitionCloseTime:this.props.transitionTime,"ms ").concat(this.props.easing),inTransition:a(e.scrollHeight)})}},{key:"openCollapsible",value:function(){this.setState({inTransition:a(this.innerRef.scrollHeight),shouldOpenOnNextCycle:!0})}},{key:"renderNonClickableTriggerElement",value:function(){return this.props.triggerSibling&&"string"==typeof this.props.triggerSibling?i.a.createElement("span",{className:"".concat(this.props.classParentString,"__trigger-sibling")},this.props.triggerSibling):this.props.triggerSibling&&"function"==typeof this.props.triggerSibling?this.props.triggerSibling():this.props.triggerSibling?i.a.createElement(this.props.triggerSibling,null):null}},{key:"render",value:function(){var e=this,t={height:this.state.height,WebkitTransition:this.state.transition,msTransition:this.state.transition,transition:this.state.transition,overflow:this.state.overflow},n=this.state.isClosed?"is-closed":"is-open",r=this.props.triggerDisabled?"is-disabled":"",s=!1===this.state.isClosed&&void 0!==this.props.triggerWhenOpen?this.props.triggerWhenOpen:this.props.trigger,o=this.props.contentContainerTagName,a=this.props.triggerTagName,c=this.props.lazyRender&&!this.state.hasBeenOpened&&this.state.isClosed&&!this.state.inTransition?null:this.props.children,u="".concat(this.props.classParentString,"__trigger ").concat(n," ").concat(r," ").concat(this.state.isClosed?this.props.triggerClassName:this.props.triggerOpenedClassName),p="".concat(this.props.classParentString," ").concat(this.state.isClosed?this.props.className:this.props.openedClassName),g="".concat(this.props.classParentString,"__contentOuter ").concat(this.props.contentOuterClassName),h="".concat(this.props.classParentString,"__contentInner ").concat(this.props.contentInnerClassName);return i.a.createElement(o,l({className:p.trim()},this.props.containerElementProps),i.a.createElement(a,l({className:u.trim(),onClick:this.handleTriggerClick,style:this.props.triggerStyle&&this.props.triggerStyle,onKeyPress:function(t){var n=t.key;(" "===n&&"button"!==e.props.triggerTagName.toLowerCase()||"Enter"===n)&&e.handleTriggerClick(t)},tabIndex:this.props.tabIndex&&this.props.tabIndex},this.props.triggerElementProps),s),this.renderNonClickableTriggerElement(),i.a.createElement("div",{className:g.trim(),style:t,onTransitionEnd:this.handleTransitionEnd,ref:this.setInnerRef,hidden:this.props.contentHiddenWhenClosed&&this.state.isClosed&&!this.state.inTransition},i.a.createElement("div",{className:h.trim()},c)))}}])&&u(t.prototype,n),r&&u(t,r),o}(r.Component);m.propTypes={transitionTime:o.a.number,transitionCloseTime:o.a.number,triggerTagName:o.a.string,easing:o.a.string,open:o.a.bool,containerElementProps:o.a.object,triggerElementProps:o.a.object,classParentString:o.a.string,openedClassName:o.a.string,triggerStyle:o.a.object,triggerClassName:o.a.string,triggerOpenedClassName:o.a.string,contentOuterClassName:o.a.string,contentInnerClassName:o.a.string,accordionPosition:o.a.oneOfType([o.a.string,o.a.number]),handleTriggerClick:o.a.func,onOpen:o.a.func,onClose:o.a.func,onOpening:o.a.func,onClosing:o.a.func,onTriggerOpening:o.a.func,onTriggerClosing:o.a.func,trigger:o.a.oneOfType([o.a.string,o.a.element]),triggerWhenOpen:o.a.oneOfType([o.a.string,o.a.element]),triggerDisabled:o.a.bool,lazyRender:o.a.bool,overflowWhenOpen:o.a.oneOf(["hidden","visible","auto","scroll","inherit","initial","unset"]),contentHiddenWhenClosed:o.a.bool,triggerSibling:o.a.oneOfType([o.a.element,o.a.func]),tabIndex:o.a.number,contentContainerTagName:o.a.string},m.defaultProps={transitionTime:400,transitionCloseTime:null,triggerTagName:"span",easing:"linear",open:!1,classParentString:"Collapsible",triggerDisabled:!1,lazyRender:!1,overflowWhenOpen:"hidden",contentHiddenWhenClosed:!1,openedClassName:"",triggerStyle:null,triggerClassName:"",triggerOpenedClassName:"",contentOuterClassName:"",contentInnerClassName:"",className:"",triggerSibling:null,onOpen:function(){},onClose:function(){},onOpening:function(){},onClosing:function(){},onTriggerOpening:function(){},onTriggerClosing:function(){},tabIndex:null,contentContainerTagName:"div"},t.default=m}]))},773:function(e,t,n){},774:function(e,t,n){"use strict";var r=n(37),i=n(39);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=i(n(0)),o=(0,r(n(40)).default)(s.createElement("path",{d:"M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"}),"ExpandLess");t.default=o},776:function(e,t,n){"use strict";n.d(t,"a",(function(){return l}));var r=n(33),i=n.n(r),s=n(57),o=n(13),a=n(0),c=n(88),l=function(e,t,n){var r=Object(a.useState)([]),l=Object(o.a)(r,2),u=l[0],p=l[1],g=Object(a.useState)(!0),h=Object(o.a)(g,2),f=h[0],d=h[1];return Object(a.useEffect)((function(){(function(){var r=Object(s.a)(i.a.mark((function r(){var s,o;return i.a.wrap((function(r){for(;;)switch(r.prev=r.next){case 0:if(!(e&&t&&n)){r.next=15;break}return d(!0),r.prev=2,s=n.map((function(n){return c.b("services/".concat(e,"/resources/").concat(t,"/").concat(n))})),r.next=6,Promise.all(s);case 6:o=r.sent,console.info("useResources response",e,t,n,o),p(o),r.next=14;break;case 11:r.prev=11,r.t0=r.catch(2),console.error(r.t0.message);case 14:d(!1);case 15:case"end":return r.stop()}}),r,null,[[2,11]])})));return function(){return r.apply(this,arguments)}})()()}),[n]),{data:u,loading:f}}}}]);
//# sourceMappingURL=9.4731a14c.chunk.js.map