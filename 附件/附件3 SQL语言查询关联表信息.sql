--收入确认单对应的业务单及核销   
select a.plywdbh 批量业务单编号,
       a.ywdbh   业务单编号,
       r.sksqdbh 收入确认单编号,
       a.khdwmc  客户单位名称,
       fp.fph    发票号,
       r.hxdate  收入核销日期
  from container_xhsrkzxb a, receive_sksqdzb r, RECEIVE_SKSQDFPXB fp
 where a.srqrdid = r.id
   and a.srqrdid = fp.sksqdzbid
   and fp.sksqdzbid = r.id
   and r.yxflag = '1'
   and fp.yxflag = '1'
 group by r.sksqdbh,
          a.plywdbh,
          a.ywdbh,
          a.srqrdbh,
          a.khdwmc,
          fp.fph,
          r.hxdate;


--成本确认单对应的业务单及核销日期        
select c.plywdbh  批量业务单编号,
       c.ywdbh    业务单编号,
       p.fksqdbh  成本确认单编号,
       c.gysmc    供应商名称,
       fk.hkdate  成本核销日期,
       fk.yhhklsh 银行付款流水
  from container_xhcbkzxb c, pay_fksqdzb p, pay_fktzdzb fk
 where c.cbqrdid = p.id
   and p.fksqdbh = fk.fkyjdjbh
   and c.cbqrdbh = fk.fkyjdjbh
   and p.yxflag = '1'
   and fk.yxflag = '1'
 group by c.plywdbh,
          c.ywdbh,
          c.cbqrdbh,
          c.gysmc,
          p.fksqdbh,
          fk.hkdate,
          fk.yhhklsh;


--收入成本相对应的业务单
select x.plywdbh  as 批量业务单编号,
       x.ywdbh    业务单编号,
       x.khdwmc   客户单位名称,
       x.sksqdbh  收入确认单编号,
       x.fph      发票号,
       x.hxdate   收入核销日期,
       e.gysmc    供应商名称,
       e.fksqdbh  成本确认单编号,
       e.yhhklsh  银行付款流水,
       e.hkdate   成本核销日期,
       y.blfcdate 发车日期
  from (select a.plywdbh, a.ywdbh, r.sksqdbh, a.khdwmc, fp.fph, r.hxdate
          from container_xhsrkzxb a, receive_sksqdzb r, RECEIVE_SKSQDFPXB fp
         where a.srqrdid = r.id
           and a.srqrdid = fp.sksqdzbid
           and fp.sksqdzbid = r.id
           and r.yxflag = '1'
           and fp.yxflag = '1'
         group by r.sksqdbh,
                  a.plywdbh,
                  a.ywdbh,
                  a.srqrdbh,
                  a.khdwmc,
                  fp.fph,
                  r.hxdate) x
  full join (select c.plywdbh,
                    c.ywdbh,
                    p.fksqdbh,
                    c.gysmc,
                    fk.hkdate,
                    fk.yhhklsh
               from container_xhcbkzxb c, pay_fksqdzb p, pay_fktzdzb fk
              where c.cbqrdid = p.id
                and p.fksqdbh = fk.fkyjdjbh
                and c.cbqrdbh = fk.fkyjdjbh
                and p.yxflag = '1'
                and fk.yxflag = '1'
              group by c.plywdbh,
                       c.ywdbh,
                       c.cbqrdbh,
                       c.gysmc,
                       p.fksqdbh,
                       fk.hkdate,
                       fk.yhhklsh) e
    on x.ywdbh = e.ywdbh
  left join businessdoc_ywdzb y
    on x.ywdbh = y.ywdbh
   and e.ywdbh = y.ywdbh;