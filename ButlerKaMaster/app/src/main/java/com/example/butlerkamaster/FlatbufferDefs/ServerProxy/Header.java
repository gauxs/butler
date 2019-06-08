// automatically generated by the FlatBuffers compiler, do not modify

package com.example.butlerkamaster.FlatbufferDefs.ServerProxy;

import java.nio.*;
import java.lang.*;
import java.util.*;
import com.google.flatbuffers.*;

@SuppressWarnings("unused")
public final class Header extends Table {
  public static Header getRootAsHeader(ByteBuffer _bb) { return getRootAsHeader(_bb, new Header()); }
  public static Header getRootAsHeader(ByteBuffer _bb, Header obj) { Constants.FLATBUFFERS_1_11_1(); _bb.order(ByteOrder.LITTLE_ENDIAN); return (obj.__assign(_bb.getInt(_bb.position()) + _bb.position(), _bb)); }
  public void __init(int _i, ByteBuffer _bb) { bb_pos = _i; bb = _bb; vtable_start = bb_pos - bb.getInt(bb_pos); vtable_size = bb.getShort(vtable_start); }
  public Header __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }

  public String country() { int o = __offset(4); return o != 0 ? __string(o + bb_pos) : null; }
  public ByteBuffer countryAsByteBuffer() { return __vector_as_bytebuffer(4, 1); }
  public ByteBuffer countryInByteBuffer(ByteBuffer _bb) { return __vector_in_bytebuffer(_bb, 4, 1); }
  public String state() { int o = __offset(6); return o != 0 ? __string(o + bb_pos) : null; }
  public ByteBuffer stateAsByteBuffer() { return __vector_as_bytebuffer(6, 1); }
  public ByteBuffer stateInByteBuffer(ByteBuffer _bb) { return __vector_in_bytebuffer(_bb, 6, 1); }
  public String city() { int o = __offset(8); return o != 0 ? __string(o + bb_pos) : null; }
  public ByteBuffer cityAsByteBuffer() { return __vector_as_bytebuffer(8, 1); }
  public ByteBuffer cityInByteBuffer(ByteBuffer _bb) { return __vector_in_bytebuffer(_bb, 8, 1); }
  public String source() { int o = __offset(10); return o != 0 ? __string(o + bb_pos) : null; }
  public ByteBuffer sourceAsByteBuffer() { return __vector_as_bytebuffer(10, 1); }
  public ByteBuffer sourceInByteBuffer(ByteBuffer _bb) { return __vector_in_bytebuffer(_bb, 10, 1); }
  public String dest() { int o = __offset(12); return o != 0 ? __string(o + bb_pos) : null; }
  public ByteBuffer destAsByteBuffer() { return __vector_as_bytebuffer(12, 1); }
  public ByteBuffer destInByteBuffer(ByteBuffer _bb) { return __vector_in_bytebuffer(_bb, 12, 1); }

  public static int createHeader(FlatBufferBuilder builder,
      int countryOffset,
      int stateOffset,
      int cityOffset,
      int sourceOffset,
      int destOffset) {
    builder.startTable(5);
    Header.addDest(builder, destOffset);
    Header.addSource(builder, sourceOffset);
    Header.addCity(builder, cityOffset);
    Header.addState(builder, stateOffset);
    Header.addCountry(builder, countryOffset);
    return Header.endHeader(builder);
  }

  public static void startHeader(FlatBufferBuilder builder) { builder.startTable(5); }
  public static void addCountry(FlatBufferBuilder builder, int countryOffset) { builder.addOffset(0, countryOffset, 0); }
  public static void addState(FlatBufferBuilder builder, int stateOffset) { builder.addOffset(1, stateOffset, 0); }
  public static void addCity(FlatBufferBuilder builder, int cityOffset) { builder.addOffset(2, cityOffset, 0); }
  public static void addSource(FlatBufferBuilder builder, int sourceOffset) { builder.addOffset(3, sourceOffset, 0); }
  public static void addDest(FlatBufferBuilder builder, int destOffset) { builder.addOffset(4, destOffset, 0); }
  public static int endHeader(FlatBufferBuilder builder) {
    int o = builder.endTable();
    return o;
  }
}

