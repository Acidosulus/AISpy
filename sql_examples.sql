select row_id, Счета, Фамилия, [stack].[AddrLs](row_id,0) from stack.[Лицевые счета] where [Счета]=-10;

select [stack].[AddrLs](row_id,0), * from stack.[Лицевые счета] where [Счета]=460353;

select [stack].[AddrLs](row_id,0), * from stack.[Лицевые счета] where [Счета]=460362;

select [stack].[AddrLs](row_id,0), * from stack.[Лицевые счета] where [Счета]=27;