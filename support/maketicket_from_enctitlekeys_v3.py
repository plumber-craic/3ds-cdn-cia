import binascii
import struct
import os
import sys

#updated for py3 syntax and wrapped in main for easy import. plumber_craic, March 7, 2019
def main(title_dir, enckeyfilename):
    tik_template = binascii.a2b_base64('AAEABP'+('\/'*340)+'8'+('A'*79)+'BSb290LUNBMDAwMDAwMDMtWFMwMDAwMDAwYw'+('A'*50)+('\/'*80)+'AQAAPC1FbmMgS2V5IEhlcmUtPg'+('A'*16)+'BUaXRsZV9JRAAAVlY'+('A'*76)+'B'+('A'*175)+'BABQAAACsAAAAFAABABQAAAAAAAAAKAAAAAEAAACEAAAAhAADAAAAAAAA'+('\/'*170)+'8=')
    tik_cert_ch1 = binascii.a2b_base64('AAEABJGevkZK0PVSzRty54hJEM9VqfAuUHiWQdiWaD3ABb0K6ocHnYrChMZ1Bl90yL83yIBEQJUCoCKYC7itSDg/bSinneOWJsyysioPGeQQMvCUs5/wEzFG3sj2wanVXNKNnhxHs9EfT1QmwseAE1onddPKZ5vH6DTw4PtY5ohgpxMw/JV5F5PI+6k1p6aQjyKd7ioMprmyOxLUlab+GdDXJkghaHhgWmZTjb83aJmQXTRF/Fxyeg4T4OLIlxyc+mxgZ4h1cypOdVI9L1YvEqq9FXO/BslAVK76gacUF6+aSgZtD/xa1kurKLH/YGYfRDfUnh4NlBLrS8rPTP1qNAiEeYI'+('A'*79)+'BSb290LUNBMDAwMDAwMDM'+('A'*70)+'VhTMDAwMDAwMGM'+('A'*72)+'TegiUrVBbtsZ+LlvdajvsQ9kQx3LpzCkNpYWIt33MEWgLs+KfTqu7JumMJgGYXAQbsUN45okYGq13BWjpKKK5gWfuPhDQcr7vH6Ivoqo+E/EeGDapKkKB73Cq9ORimYIhxvu5vdAX5qxZBJTpzqmFnOstKkwXZvLDORLFjxSoA+NvzNzM3BP9eud8enjZl+asw1VX4NPp62S0PJL0xQ1npgLes5GwZmHNMogL1kkSrxy8txYqBvAlZdOw7OT87N2uikk0247mfzAXmGIhFV0THGw/CasZRcIGrHDJQrNvSaEYO814tuS0fGxcrA+NYviXxpU90S8otwxbffdRgZqYNGUmJQABAAE'+('A'*69))
    tik_cert_ch2 = binascii.a2b_base64('AAEAA3BBOO+7vaFqmH3ZATJtHJRZSEyIooYbkaMSWHrnDvYjfsUOEDLcOd3ompao6FnXapim5+NqDP41LKiTBYI0/4M/yzsDgR6fDcDZpS+ARbSy+UEbZ6UcRLXvjOd71tVrp1c0oYVt5tS+1tOiQsfIeRs0IjdeXHeavwcvdpXvoPdby4N4n8MOP+TMg5IgeEBjiUnH9ohWX2SbdNY9jVj/rdpXHpVUQmsTGPxGiYPUyKViiwa2/F1QfBPnoYrBUR621i6lRI+DUBRHqa+z7MKQPJ3VL5Iqyazb71jGAhhI2W4ghzLT0dnZ6kQNkWIcepnbiEPFnB8uLH2bV31RLBZtb34arUp3SjdEfnj+ICHhSpXREqBoraAZ9GPHpVaFqrtoiLkkZIPRi5yAb0dJGDMXgjRKS4UxM0smMDJj2dLrT0u5lgKzUvauQEbGml5+jkoY75vAot7WExBBcBL9gkzBFs+3xMH37HF3oXRGy96W8+3Yj80FLwuIikX9rytjE1T0DRbl+pwsTtqY55jRXmBG3FNj8wlrLGB6nY3VWxUCpqx9PMjYxXWZjn15aRDIBMSVI1BX6R7NJjfJwYRRUaxrmgSQrj7G9HdAoNsLo20HWVbO5zVOo+mk8nILJlUMfTlDJLwMt+kxfYqGYfQhkf8QsIJWzj/SW3ReUZSQa01hy0wu'+('A'*80)+'Um9vd'+('A'*85)+'FDQTAwMDAwMDAz'+('A'*72)+'e+jvbLJ5yeLu4SHG6vRP9jn4jweLS3ftn5VgsDWCgbUOVatyERWhd3A8ejD+OunvHGC8HZdGdrI6aMwEsZhSW8lo8R3i21Dk2efwceVi2uIJIjPp02P2HdfBn/OkqR6PZVPUcd17hLnxuM5zNfD1VAVjoeq4OWPgm+kBAR+ZVGNhKHAg6cwNq0h/FA1mJqGDbScRHyBo3kdyFJFRz2nGG6YO+dlJoPcfVJny05rSjHAFNIKTxDH/vTP2vKYNxxleorzFbSALr20G0JxB243pxyAVTKSDK2nAjGnNOwc6AGNgL0YtM4BhpepskVzVYjV5w+tkzkTvWG0UuqqINAGbPuvu03kAAQAB'+('A'*70)+'==')
    
    tmdfilename = os.path.join(os.path.abspath(title_dir), 'title.tmd')
    if not os.path.exists(tmdfilename):
        tmdfilename = os.path.join(os.path.abspath(title_dir), 'tmd')
    enckeyfilename = os.path.abspath(enckeyfilename)    
    if os.path.exists(os.path.abspath(tmdfilename)):
        with open (os.path.abspath(tmdfilename), 'rb') as tmdfile:
            tmddata = tmdfile.read()
            if tmddata[0x0000:0x0004] == b'\x00\x01\x00\x04':
                tmdver = int(binascii.b2a_hex(tmddata[0x1DC:0x1DE]), 16)                
                if os.path.exists(enckeyfilename):
                    with open(enckeyfilename, 'rb') as enckeydb:
                        numenckeys = struct.unpack("<LLLL", enckeydb.read(0x10))
                        for key in range (0, numenckeys[0]):
                            foundkey = 0
                            enckeykeytype = enckeydb.read(0x04)
                            enckeyjunk = enckeydb.read(0x04)
                            enckeytitleid = enckeydb.read(0x08)                            
                            enckeydata = enckeydb.read(0x10)
                            if enckeytitleid == tmddata[0x018C:0x0194]:
                                foundkey = 1
                                tikdata = bytearray(tik_template)
                                tikdata[0x01DC:0x01E4] = tmddata[0x018C:0x0194]
                                tikdata[0x01E6:0x01E8] = tmddata[0x01DC:0x01DE]
                                tikdata[0x01BF:0x01CF] = enckeydata[0x0000:0x0010]
                                open(os.path.join(os.path.abspath(os.path.dirname(tmdfilename)), "cetk") ,'wb').write(tikdata+tik_cert_ch1+tik_cert_ch2)
                                # predictable cert names
                                #if os.path.basename(tmdfilename) == "tmd":
                                #    open(os.path.join(os.path.abspath(os.path.dirname(tmdfilename)), "cetk") ,'wb').write(tikdata+tik_cert_ch1+tik_cert_ch2)
                                #else:
                                #    open(os.path.join(os.path.abspath(os.path.dirname(tmdfilename)), "cetk." + str(tmdver)),'wb').write(tikdata+tik_cert_ch1+tik_cert_ch2)                            
                                #print("CETK Ticket created successfully...")
                                return 0                                
                        if foundkey == 0:
                            print("Encrypted Titlekey not found in encTitleKeys.bin...")
                            return 1                           
                else:
                    print("encTitleKeys.bin file not found...")
                    return 1
            else:
                print("file doesn't appear to be a valid tmd...")
                return 1
    else:
        print("tmd file not found...")
        return 1
        
if __name__ == "__main__":
    main()
