package project;
import java.math.BigInteger;
public class test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String _str_one = "4b64ca12ace755516c178f72d05d7061";
        String _str_two = "ecd44646cfe5994ebeb35bf922e25dba";
		BigInteger i1 = new BigInteger(_str_one, 16);
	    BigInteger i2 = new BigInteger(_str_two, 16);
	    BigInteger res = i1.xor(i2);
	    String result = res.toString(16);
	    System.out.println("your flag is: " +result);

	}

}
