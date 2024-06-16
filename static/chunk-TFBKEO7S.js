import{I as ke,J as Be,K as Ve,L as Ne,M as qe,N as He,O as je,P as Ue,Q as ze,R as Le,S as We,T as Qe,V as Ze,W as $,f as oe,g as re,h as ae,i as le,j as se,k as ce,l as ue,n as _e,o as fe,q as Ce,r as be,t as xe,u as he,w as ge,y as Te,z as Se}from"./chunk-LOREQPXC.js";import{Ba as $e,Da as Pe,Ia as R,Y as ee,ca as me,ea as pe,fa as de,ga as De,ha as ve,ja as Ee,la as V,na as Oe,oa as Me,pa as we,ra as N,sa as ye,ta as Ge,ua as Ie,va as Ae,xa as Fe,ya as Re}from"./chunk-Z4ZXHPEY.js";import{$b as Z,Ab as y,Bb as G,Cb as o,Db as n,Eb as _,Fb as f,Gb as C,Hb as W,Hc as K,Ib as I,Ic as X,Kc as Y,Lb as g,Lc as F,N as j,Nb as c,Tc as te,Ub as Q,Uc as ie,Vb as l,Wb as v,Wc as k,Xb as E,Xc as B,Ya as p,Za as u,Zc as ne,_b as T,ac as A,cc as S,dc as D,ec as J,ka as h,lb as U,rb as d,sa as O,sb as z,t as H,ta as M,tb as s,vb as L,yb as x,zb as w}from"./chunk-ORS3OGVJ.js";var P=class e{constructor(t){this.orders=[],Object.assign(this,t)}static createFromApiModel(t){return new e({id:t.id,createdAt:t.created_at,hostMember:t.host_member,status:t.status,actualAmount:t.actual_amount,orders:t.orders.map(i=>Se.createFromApiModel(i))})}get total(){return this.orders.reduce((t,i)=>t+i.subtotal,0)}get totalCount(){return this.orders.reduce((t,i)=>t+i.totalCount,0)}};var q=function(e){return e.InProgress="in_progress",e.Completed="completed",e.Cancelled="cancelled",e}(q||{});function tt(e,t){if(e&1&&(o(0,"mat-option",4),l(1),n()),e&2){let i=t.$implicit;s("value",i.id),p(),v(i.orderedBy)}}var Ke=(()=>{let t=class t{constructor(r,a,m){this.data=r,this._groupOrderService=a,this._dialogRef=m,this.isSubmitting=!1,this._constructForm()}_constructForm(){this.mainForm=new we({orders:new N(this.data.orders.map(r=>r.id)),actualAmount:new N(this.data.total,[V.required,V.min(0)])})}completeOrder(){let r={orders:this.mainForm.value.orders,actual_amount:this.mainForm.value.actualAmount};this.isSubmitting=!0,this._groupOrderService.complete(this.data.id,r).pipe(j(()=>this.isSubmitting=!1)).subscribe(()=>{this._dialogRef.close(this.data.id)})}};t.\u0275fac=function(a){return new(a||t)(u(je),u($),u(He))},t.\u0275cmp=h({type:t,selectors:[["app-complete-group-order-dialog"]],standalone:!0,features:[T],decls:19,vars:3,consts:[["mat-dialog-title",""],[3,"formGroup"],[1,"w-100"],["formControlName","orders","multiple",""],[3,"value"],["matInput","","formControlName","actualAmount","type","number"],["align","end"],["mat-raised-button","","mat-dialog-close","",1,"mr-2"],[3,"action","disabled","isSubmitting"]],template:function(a,m){a&1&&(o(0,"h2",0),l(1,"Complete order"),n(),o(2,"mat-dialog-content")(3,"form",1)(4,"mat-form-field",2)(5,"mat-label"),l(6,"Orders"),n(),o(7,"mat-select",3),y(8,tt,2,2,"mat-option",4,w),n()(),o(10,"mat-form-field",2)(11,"mat-label"),l(12,"Actual amount"),n(),_(13,"input",5),n()()(),o(14,"mat-dialog-actions",6)(15,"button",7),l(16,"Close"),n(),o(17,"app-submit-button",8),g("action",function(){return m.completeOrder()}),l(18,"Complete "),n()()),a&2&&(p(3),s("formGroup",m.mainForm),p(5),G(m.data.orders),p(9),s("disabled",!m.mainForm.valid)("isSubmitting",m.isSubmitting))},dependencies:[Le,We,Qe,me,$e,Re,Pe,Fe,ye,Ee,Ge,Oe,Me,Ie,Ae,Ze,ze,ke,ee]});let e=t;return e})();var ot=()=>["expandedDetail"],rt=e=>({$implicit:e});function at(e,t){e&1&&(o(0,"th",16),l(1," Time "),n())}function lt(e,t){if(e&1&&(o(0,"td",17),l(1),S(2,"date"),n()),e&2){let i=t.$implicit;p(),E(" ",D(2,1,i.createdAt)," ")}}function mt(e,t){e&1&&(o(0,"th",16),l(1," Host "),n())}function pt(e,t){if(e&1&&(o(0,"td",17),l(1),n()),e&2){let i=t.$implicit;p(),E(" ",i.hostMember.name," ")}}function dt(e,t){e&1&&(o(0,"th",16),l(1," Actual amount "),n())}function st(e,t){if(e&1&&(o(0,"td",17),l(1),n()),e&2){let i=t.$implicit;p(),E(" ",i.actualAmount," ")}}function ct(e,t){e&1&&(o(0,"th",16),l(1," Status "),n())}function ut(e,t){if(e&1&&(o(0,"td",17),l(1),n()),e&2){let i=t.$implicit;p(),E(" ",i.status," ")}}function _t(e,t){e&1&&(o(0,"th",16),l(1," Actions "),n())}function ft(e,t){if(e&1){let i=I();o(0,"button",19),g("click",function(a){O(i);let m=c().$implicit,b=c();return a.stopPropagation(),M(b.complete(m))}),o(1,"mat-icon"),l(2,"task_alt"),n()()}}function Ct(e,t){if(e&1&&(o(0,"td",17),d(1,ft,3,0,"button",18),n()),e&2){let i=t.$implicit,r=c();p(),x(r.currentUserId===i.hostMember.id&&i.status===r.OrderStatusEnum.InProgress?1:-1)}}function bt(e,t){e&1&&(o(0,"th",20),l(1,"\xA0"),n())}function xt(e,t){e&1&&(o(0,"mat-icon"),l(1,"keyboard_arrow_up"),n())}function ht(e,t){e&1&&(o(0,"mat-icon"),l(1,"keyboard_arrow_down"),n())}function gt(e,t){if(e&1){let i=I();o(0,"td",17)(1,"button",21),g("click",function(a){let m=O(i).$implicit,b=c();return b.expandedElement=b.expandedElement===m?null:m,M(a.stopPropagation())}),d(2,xt,2,0,"mat-icon")(3,ht,2,0,"mat-icon"),n()()}if(e&2){let i=t.$implicit,r=c();p(2),x(r.expandedElement===i?2:3)}}function Tt(e,t){e&1&&W(0)}function St(e,t){if(e&1&&(o(0,"td",17)(1,"div",22),d(2,Tt,1,0,"ng-container",23),n()()),e&2){let i=t.$implicit,r=c(),a=Q(26);z("colspan",r.columnsToDisplayWithExpand.length),p(),s("@detailExpand",i==r.expandedElement?"expanded":"collapsed"),p(),s("ngTemplateOutlet",a)("ngTemplateOutletContext",A(4,rt,i.orders))}}function Dt(e,t){e&1&&_(0,"tr",24)}function vt(e,t){if(e&1){let i=I();o(0,"tr",25),g("click",function(){let a=O(i).$implicit,m=c();return M(m.expandedElement=m.expandedElement===a?null:a)}),n()}if(e&2){let i=t.$implicit,r=c();L("expanded-row",r.expandedElement===i)}}function Et(e,t){e&1&&_(0,"tr",26)}function Ot(e,t){if(e&1&&(o(0,"tr")(1,"td"),l(2),n(),o(3,"td"),l(4),n()()),e&2){let i=t.$implicit;p(2),v(i.orderedBy),p(2),v(i.subtotal)}}function Mt(e,t){if(e&1&&(o(0,"table")(1,"tr")(2,"th"),l(3,"Member"),n(),o(4,"th"),l(5,"Total"),n()(),y(6,Ot,5,2,"tr",null,w),n()),e&2){let i=c().$implicit;p(6),G(i)}}function wt(e,t){if(e&1&&(o(0,"div"),d(1,Mt,8,0,"table"),n()),e&2){let i=t.$implicit;p(),x(i.length>0?1:-1)}}var Xe=(()=>{let t=class t extends Ne{constructor(r,a,m){super(),this._groupOrderService=r,this._appData=a,this._dialog=m,this.OrderStatusEnum=q,this.columnsToDisplay=["time","host","amount","status","actions"],this.columnsToDisplayWithExpand=[...this.columnsToDisplay,"expand"],this._appData.currentUser$.subscribe(b=>this.currentUserId=b.id),this._queryRequest=this._constructQueryRequest.bind(this)}_constructQueryRequest(){return this._groupOrderService.query(this.queryParams??{}).pipe(H(r=>r.map(a=>P.createFromApiModel(a))))}complete(r){this._dialog.open(Ke,{data:r}).afterClosed().subscribe(()=>this.refresh())}};t.\u0275fac=function(a){return new(a||t)(u($),u(R),u(Ue))},t.\u0275cmp=h({type:t,selectors:[["app-group-orders-table"]],inputs:{queryParams:"queryParams"},standalone:!0,features:[U,T],decls:27,vars:7,consts:[["orderDetails",""],["mat-table","","multiTemplateDataRows","",3,"dataSource"],["matColumnDef","time"],["mat-header-cell","",4,"matHeaderCellDef"],["mat-cell","",4,"matCellDef"],["matColumnDef","host"],["matColumnDef","amount"],["matColumnDef","status"],["matColumnDef","actions"],["matColumnDef","expand"],["mat-header-cell","","aria-label","row actions",4,"matHeaderCellDef"],["matColumnDef","expandedDetail"],["mat-header-row","",4,"matHeaderRowDef"],["mat-row","","class","expanding-row",3,"expanded-row","click",4,"matRowDef","matRowDefColumns"],["mat-row","","class","detail-row",4,"matRowDef","matRowDefColumns"],["showFirstLastButtons","","aria-label","Select page",3,"pageSize","pageSizeOptions"],["mat-header-cell",""],["mat-cell",""],["mat-icon-button","","color","warn","aria-label","Complete","matTooltip","Complete"],["mat-icon-button","","color","warn","aria-label","Complete","matTooltip","Complete",3,"click"],["mat-header-cell","","aria-label","row actions"],["mat-icon-button","","aria-label","expand row",3,"click"],[1,"expanding-row-detail"],[4,"ngTemplateOutlet","ngTemplateOutletContext"],["mat-header-row",""],["mat-row","",1,"expanding-row",3,"click"],["mat-row","",1,"detail-row"]],template:function(a,m){a&1&&(o(0,"table",1),f(1,2),d(2,at,2,0,"th",3)(3,lt,3,3,"td",4),C(),f(4,5),d(5,mt,2,0,"th",3)(6,pt,2,1,"td",4),C(),f(7,6),d(8,dt,2,0,"th",3)(9,st,2,1,"td",4),C(),f(10,7),d(11,ct,2,0,"th",3)(12,ut,2,1,"td",4),C(),f(13,8),d(14,_t,2,0,"th",3)(15,Ct,2,1,"td",4),C(),f(16,9),d(17,bt,2,0,"th",10)(18,gt,4,1,"td",4),C(),f(19,11),d(20,St,3,6,"td",4),C(),d(21,Dt,1,0,"tr",12)(22,vt,1,2,"tr",13)(23,Et,1,0,"tr",14),n(),_(24,"mat-paginator",15),d(25,wt,2,1,"ng-template",null,0,J)),a&2&&(s("dataSource",m.dataSource),p(21),s("matHeaderRowDef",m.columnsToDisplayWithExpand),p(),s("matRowDefColumns",m.columnsToDisplayWithExpand),p(),s("matRowDefColumns",Z(6,ot)),p(),s("pageSize",m.DEFAULT_PAGINATOR_PAGE_SIZE)("pageSizeOptions",m.PAGINATOR_SIZE_OPTIONS))},dependencies:[Te,se,ue,be,_e,ce,xe,fe,Ce,he,ge,de,pe,ve,De,qe,Y,Ve,Be,F,K],data:{animation:[te("detailExpand",[B("collapsed,void",k({height:"0px",minHeight:"0"})),B("expanded",k({height:"*"})),ne("expanded <=> collapsed",ie("225ms cubic-bezier(0.4, 0.0, 0.2, 1)"))])]}});let e=t;return e})();var yt=e=>({host_member:e});function Gt(e,t){e&1&&_(0,"app-group-orders-table")}function It(e,t){e&1&&(o(0,"div",3),l(1,"Login to view content."),n())}function At(e,t){if(e&1&&(_(0,"app-group-orders-table",6),S(1,"async")),e&2){let i,r=c(2);s("queryParams",A(3,yt,(i=D(1,1,r.currentUser$))==null?null:i.id))}}function Ft(e,t){e&1&&(o(0,"div",3),l(1,"Login to view content."),n())}function Rt(e,t){if(e&1&&(d(0,At,2,5,"app-group-orders-table",6),S(1,"async"),d(2,Ft,2,0,"div",3)),e&2){let i=c();x(D(1,1,i.currentUser$)?0:2)}}var fi=(()=>{let t=class t{constructor(r){this._appData=r,this.currentUser$=this._appData.currentUser$}};t.\u0275fac=function(a){return new(a||t)(u(R))},t.\u0275cmp=h({type:t,selectors:[["app-group-orders-dashboard"]],standalone:!0,features:[T],decls:9,vars:3,consts:[[1,"text-align-center"],["mat-stretch-tabs","false","mat-align-tabs","start"],["label","All"],[1,"m-4"],["label","Mine"],["matTabContent",""],[3,"queryParams"]],template:function(a,m){a&1&&(o(0,"h1",0),l(1,"Group orders"),n(),o(2,"mat-tab-group",1)(3,"mat-tab",2),d(4,Gt,1,0,"app-group-orders-table"),S(5,"async"),d(6,It,2,0,"div",3),n(),o(7,"mat-tab",4),d(8,Rt,3,3,"ng-template",5),n()()),a&2&&(p(4),x(D(5,1,m.currentUser$)?4:6))},dependencies:[le,oe,re,ae,F,X,Xe]});let e=t;return e})();export{fi as GroupOrdersDashboardComponent};
