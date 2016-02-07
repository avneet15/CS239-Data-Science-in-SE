import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Stack;
//implementation 2 to include annotation, max depth, and global method count
public class Node {
	static int maxDepth=0;
	static Stack<String> stack=new Stack<String>();
	static HashMap<String,HashMap<String,Integer>> map=new HashMap<String,HashMap<String,Integer>>();
	static HashMap<String,Integer> globalMethodCount=new HashMap<String,Integer>();
	static HashMap<String,Integer> globalKLenMap=new HashMap<String,Integer>();
	static HashMap<String,Integer> globalGenericKLengthMap=new HashMap<String,Integer>();
	static int MAX_K=100;
	//second hashmap has string which parent+depth and value is the count
	static int errorCount=0;
	
	public static void main(String[] args) {
		try(BufferedReader reader=new BufferedReader(new FileReader(args[0]))){
			
			String line=reader.readLine();
			PrintToFile writeCallingContextTree=new PrintToFile();
			writeCallingContextTree.initialisefile("/home/ms/git/jline_outputCCT.txt");
			while((line=reader.readLine())!=null){
				if(!line.contains("[Call") && line.contains("Exception")){
					int i=0;
					String line_CCT="";
					//commented for now
					addExceptionToCCT(writeCallingContextTree, i, line_CCT);
					errorCount++;
				}
				while(line!=null && !line.contains("[Call")){
					line=reader.readLine();
				}
				if(line!=null)formatLine(line,writeCallingContextTree);
			}
			writeCallingContextTree.closeFile();
			extractGlobalMethodCount();
			
			//for global k length
			extractGlobalK2Sequence();
			extractKLengthSeq_Generic();
			
			System.out.println("No of Exceptions: "+errorCount);
			System.out.println("Max Depth: "+maxDepth);
		}
		catch(Exception e){
			System.out.println("An Error occured!");
			e.printStackTrace();
			return;
		}
	}
	
	private static void extractKLengthSeq_Generic() throws IOException{
		PrintToFile globalKLengthFile= new PrintToFile();
		globalKLengthFile.initialisefile("/home/ms/git/jline_outputKSeq_Generic_length100.txt");
		globalKLengthFile.getGlobalCounts(globalKLengthFile,globalGenericKLengthMap);
		globalKLengthFile.closeFile();
	}

	private static void extractGlobalK2Sequence() throws IOException {
		PrintToFile globalSeqPrint= new PrintToFile();
		globalSeqPrint.initialisefile("/home/ms/git/jline_outputSeq.txt");
		globalSeqPrint.getGlobalCounts(globalSeqPrint,globalKLenMap);
		globalSeqPrint.closeFile();
	}

	private static void extractGlobalMethodCount() throws IOException {
		PrintToFile globalMethodPrint= new PrintToFile();
		globalMethodPrint.initialisefile("/home/ms/git/jline_outputMap.txt");
		globalMethodPrint.getGlobalCounts(globalMethodPrint,globalMethodCount);
		globalMethodPrint.closeFile();
	}

	private static void addExceptionToCCT(PrintToFile writeCallingContextTree, int i, String line_CCT)
			throws IOException {
		if(!stack.isEmpty()){
			
			for(i=0;i<stack.size();i++){
			line_CCT+="	";
		}}
		line_CCT+="<"+i+">:Exception\n";
		writeCallingContextTree.addContent(line_CCT);
	}
	
	
	
	public static void formatLine(String line,PrintToFile writeCallingContextTree) throws IOException{
		if(!stack.isEmpty()){
			maxDepth=stack.size()>maxDepth?stack.size():maxDepth;
		}
		if(line.contains(".[Call")) {
			line=line.replace(".", "");
			}
		if(line.contains("[Call begin] ")){
			line=line.replace("[Call begin] ","");
			
			
			
			addKLenSeqToMap(line);
			
			addMethodToMap(line);
			
			int lineCount=addToStackTraceMap(line);
			
			stack.push(line);
			
			//globalKlengthseq
			addToGenericKLengthSeq();
			
			//commented for now
			appendCCTAnnotationsToFile(line, writeCallingContextTree, lineCount);
			
		}
		else if(line.contains("[Call end] ")){
			//pop stack
			stack.pop();
			if(stack.isEmpty()) resetMap();
		}
	}

	private static void addToGenericKLengthSeq() {
		if(!stack.isEmpty() && stack.size()>=MAX_K){
			//store k seq in map
			Stack<String> stack_temp=new Stack<String>();
			int pop=0;
			String seq="";
			while(!stack.isEmpty() && pop!=MAX_K){
				stack_temp.push(stack.pop());
				pop++;
			}
			while(!stack_temp.isEmpty()){
				String poppedParent=stack_temp.pop();
				seq+=poppedParent;
				if(!stack_temp.isEmpty()) seq+=",";
				stack.push(poppedParent);
			}
			if(globalGenericKLengthMap.containsKey(seq)){
				int count=globalGenericKLengthMap.get(seq);
				globalGenericKLengthMap.put(seq, ++count);
			}
			else globalGenericKLengthMap.put(seq, 1);
		}
	}

	private static void appendCCTAnnotationsToFile(String line, PrintToFile writeCallingContextTree, int lineCount)
			throws IOException {
		int i=0;
		String line_CCT="";
		if(!stack.isEmpty()){
			for(i=0;i<stack.size();i++){
				line_CCT+="	";
			}}
		line_CCT+="<"+i+">:"+line+" ("+lineCount+")\n";
		writeCallingContextTree.addContent(line_CCT);
	}

	private static int addToStackTraceMap(String line) {
		int lineCount;
		if(map.containsKey(line)){
			HashMap<String,Integer> methodMap=map.get(line);
			//form parent depth combo
			String parentAndDepth="";
			if(stack.isEmpty()) parentAndDepth="root"+1;
			else parentAndDepth=stack.peek()+stack.size();
			if(methodMap.containsKey(parentAndDepth)){
				lineCount=methodMap.get(parentAndDepth);
				methodMap.put(parentAndDepth, ++lineCount);
			}
			else methodMap.put(parentAndDepth, lineCount=1);
		}
		else {
			HashMap<String,Integer> methodMap=new HashMap<String,Integer>();
			//form parent depth combo
			String parentAndDepth="";
			lineCount=1;
			if(stack.isEmpty()) parentAndDepth="root"+lineCount;
			else parentAndDepth=stack.peek()+stack.size();
			methodMap.put(parentAndDepth, lineCount);
			map.put(line, methodMap);
		}
		return lineCount;
	}

	private static void addMethodToMap(String line) {
		if(globalMethodCount.containsKey(line)){
			int method_count_temp=globalMethodCount.get(line);
			globalMethodCount.put(line, ++method_count_temp);
		}
		else globalMethodCount.put(line, 1);
	}

	private static void addKLenSeqToMap(String line) {
		if(!stack.isEmpty() && globalKLenMap.containsKey(stack.peek()+","+line)){
				String parent_child_seq=stack.peek()+","+line;
				int count=globalKLenMap.get(parent_child_seq);
				globalKLenMap.put(parent_child_seq, ++count);
		}
		else if(globalKLenMap.containsKey("root,"+line)){
				String parent_child_seq="root,"+line;
				int count=globalKLenMap.get(parent_child_seq);
				globalKLenMap.put(parent_child_seq, ++count);
			
		}
		else {
			if(!stack.isEmpty())
			globalKLenMap.put(stack.peek()+","+line,1 );
			else globalKLenMap.put("root,"+line,1);
		}
	}

	public static void resetMap(){
		map=new HashMap<String,HashMap<String,Integer>>();
	}
}
