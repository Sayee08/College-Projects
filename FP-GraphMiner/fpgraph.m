clear
filename='test1.xlsx';
sheet='bitcodes';
data=xlsread(filename,sheet);
size=11;
sizec=5;
%finding weight
for i=1:size
    ftable(i,1)= sum(data(i,1:sizec));
    ftable(i,2)= i;
end
%finding decimal equivalent
for i=1:size
    row=ftable(i,2);
    str_x=num2str(data(row,1:sizec));
    str_x(isspace(str_x))='';
    ftable(i,4)=bin2dec(str_x);
end
%sort based on decimal equivalent
[values,order]=sort(ftable(:,4),'descend');
ftable=ftable(order,:);
%finding node number
nn=1;
ftable(1,5)=nn;
for i=2:size
    if(ftable(i-1,4)==ftable(i,4))
        ftable(i,5)=ftable(i-1,5);
        ftable(i-1,2)
    else
        nn=nn+1;
        ftable(i,5)=nn;
    end
end
%sort based on weight
[values,order]=sort(ftable(:,1),'descend');
ftable=ftable(order,:);
cln=1;
ftable(1,3)=cln;
cnt=1;
clist(cln,cnt)=1;
%finding cluster number
for i=2:size
    if(ftable(i-1,1)==ftable(i,1))
        ftable(i,3)=ftable(i-1,3);
        cnt=cnt+1;
        clist(cln,cnt)=i;
    else
        cnt=cnt+1;
        clist(cln,cnt)=-1;
        cln=cln+1;
        cnt=1;
        clist(cln,cnt)=i;
        ftable(i,3)=cln;
    end
end
clist(cln,cnt+1)=-1;
%link part
cln1=cln;
cnt=1;
cn=1;
while cln1~=1
    cnt=1;
    while clist(cln1,cnt)~=-1
        cl=cln1-1;
        fl=0;
        while fl~=1 && cl~=0
            cn=1;
            while clist(cl,cn)~=-1
                if(bitand(ftable(clist(cl,cn),4),ftable(clist(cln1,cnt),4))==ftable(clist(cln1,cnt),4))
                    mat(ftable(clist(cl,cn),5),ftable(clist(cln1,cnt),5))=ftable(clist(cln1,cnt),4);
                    mat(ftable(clist(cln1,cnt),5),ftable(clist(cl,cn),5))=ftable(clist(cln1,cnt),4);
                    fl=1;
                else
                    mat(ftable(clist(cl,cn),5),ftable(clist(cln1,cnt),5))=0;
                    mat(ftable(clist(cln1,cnt),5),ftable(clist(cl,cn),5))=0;
                end
                cn=cn+1;
            end
            cl=cl-1;
        end
        cnt=cnt+1;
    end
    cln1=cln1-1;
end