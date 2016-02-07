import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class PrintToFile {
	//"/home/ms/git/outputMap_197MB.txt"
	BufferedWriter bw =null;
	public void initialisefile(String name){
		try {
			File file = new File(name);

			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}

			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			bw = new BufferedWriter(fw);

		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void addContent(String content) throws IOException{
		bw.write(content);
	}
	
	public void closeFile() throws IOException{
		bw.close();
	}
	
	public void getGlobalCounts(PrintToFile globalMethodPrint,HashMap<String,Integer> globalMethodCount) throws IOException{
		String csvLine="";
		for (Map.Entry<String,Integer> entry : globalMethodCount.entrySet()) {
			csvLine=entry.getKey()+","+entry.getValue()+"\n";
			globalMethodPrint.addContent(csvLine);
		}
	}
	
}
