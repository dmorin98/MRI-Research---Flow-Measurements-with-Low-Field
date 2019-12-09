% -----------------------------------------------------
% Reads in raw data from the NTNMR format
% modified (May 13 2009) to read file size from header
% note that NTNMR data also has a footer!
% -----------------------------------------------------
% adapted Feb 2012 from bnrreadntnmr_8va.m
% for Gordon Wilson's Honours project
% in order to be MATLAB compatible
% -----------------------------------------------------

function data=bnrgarfield(fname)

% fname is the filename you wish to open

fp=fopen(fname,'r','ieee-le'); 		% 'ieee-be' BIG endian
hdrsize=1056;
fseek(fp,36,'bof');			% determine file size from header
dims=fread(fp,4,'int32');%was 3 values to read now it is 4
fseek(fp,52,'bof');
multi = fread(fp,1,'int32'); % number of acquisition points
dims(1) = dims(1) / multi;
dims = [dims(1), dims(2), dims(3), dims(4), multi];
fseek(fp,hdrsize,'bof');

% Complex data as paired 32-bit floating point numbers

fbuffer=fread(fp,2*dims(1)*dims(2)*dims(3)*dims(4)*multi,'single');
data=fbuffer(1:2:end)+i*fbuffer(2:2:end);

data=squeeze(reshape(data,multi,dims(1)));
fclose(fp);

end % function end
